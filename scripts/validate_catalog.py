#!/usr/bin/env python3
"""
Semantic & structural validation for Backstage/Roadie catalog YAML files.

Checks:
  - Multi-document YAML handling (supports --- separators)
  - Required top-level fields: apiVersion, kind, metadata.name
  - apiVersion must equal backstage.io/v1alpha1
  - kind must be one of allowed kinds
  - metadata.name must be kebab-case (lowercase letters, numbers, hyphens) and <= 63 chars
  - Duplicate (kind, metadata.name) across all documents flagged as error
  - Optional spec.owner warning if missing for Component / System / Domain / API / Group
  - Reports summary counts by kind
  - Gracefully skips empty documents
Exit codes:
  0 = success (no errors)
  1 = errors found
Warnings do not fail build.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

import yaml

ALLOWED_KINDS = {
    "Component", "System", "Domain", "API", "Group", "Template", "Location"
}
RE_NAME = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_FILES = list((REPO_ROOT / "catalog").glob("*.yaml")) + [REPO_ROOT / "catalog-info.yaml"]

errors: List[str] = []
warnings: List[str] = []
seen: Dict[Tuple[str, str], Path] = {}
counts: Dict[str, int] = {}

def validate_document(doc: Dict[str, Any], source: Path, index: int) -> None:
    if not doc:  # Skip empty documents
        warnings.append(f"{source}: document #{index+1} is empty; skipping")
        return
    def err(msg: str):
        errors.append(f"{source} [doc {index+1}]: {msg}")
    def warn(msg: str):
        warnings.append(f"{source} [doc {index+1}]: {msg}")

    api_version = doc.get("apiVersion")
    kind = doc.get("kind")
    metadata = doc.get("metadata", {})
    name = metadata.get("name")

    # Required fields
    if not api_version:
        err("Missing apiVersion")
    elif api_version != "backstage.io/v1alpha1":
        err(f"Unexpected apiVersion '{api_version}'")

    if not kind:
        err("Missing kind")
    elif kind not in ALLOWED_KINDS:
        err(f"Kind '{kind}' not in allowed set {sorted(ALLOWED_KINDS)}")

    if not name:
        err("Missing metadata.name")
    else:
        if len(name) > 63:
            warn(f"metadata.name '{name}' longer than 63 chars")
        if not RE_NAME.match(name):
            err(f"metadata.name '{name}' not kebab-case")

    # Duplicate detection
    if kind and name:
        key = (kind, name)
        if key in seen:
            other = seen[key]
            err(f"Duplicate entity {kind}:{name} already defined in {other}")
        else:
            seen[key] = source
            counts[kind] = counts.get(kind, 0) + 1

    # Owner warnings for relevant kinds
    if kind in {"Component", "System", "Domain", "API", "Group"}:
        spec = doc.get("spec", {})
        owner = spec.get("owner")
        if not owner:
            warn(f"Kind {kind} missing spec.owner")


def main() -> int:
    print("== Catalog Semantic Validation ==")
    print(f"Scanning {len(CATALOG_FILES)} files...\n")

    for file in CATALOG_FILES:
        if not file.exists():
            warnings.append(f"Missing expected file {file}")
            continue
        try:
            with open(file, "r", encoding="utf-8") as f:
                docs = list(yaml.safe_load_all(f))
        except Exception as e:
            errors.append(f"{file}: YAML parse error: {e}")
            continue
        print(f"File: {file.relative_to(REPO_ROOT)} ({len(docs)} document(s))")
        for idx, doc in enumerate(docs):
            validate_document(doc, file, idx)

    # Summary
    print("\n== Summary ==")
    if counts:
        for kind in sorted(counts):
            print(f"  {kind}: {counts[kind]}")
    else:
        print("  No valid entities discovered.")

    if warnings:
        print("\n== Warnings ==")
        for w in warnings:
            print(f"  WARN: {w}")
    else:
        print("\nNo warnings.")

    if errors:
        print("\n== Errors ==")
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\nValidation failed with {len(errors)} error(s).")
        return 1

    print("\nAll catalog entities passed semantic validation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

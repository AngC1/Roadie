#!/usr/bin/env python3
"""
Semantic, structural & relational validation for Backstage/Roadie catalog YAML files.

Checks:
    Structure:
        - Multi-document YAML handling (supports --- separators)
        - Required top-level fields: apiVersion, kind, metadata.name
        - apiVersion must equal backstage.io/v1alpha1
        - kind must be one of allowed kinds
        - metadata.name must be kebab-case and <= 63 chars
        - Duplicate (kind, metadata.name) detection
    Ownership & relations:
        - spec.owner entity existence (group:<name>)
        - Component.spec.system reference to existing System
        - System.spec.domain reference to existing Domain
    Annotations:
        - Warn if missing github.com/project-slug on Component/System/API
        - Warn if missing backstage.io/techdocs-ref on Component/System
    Reporting:
        - Summary counts by kind
        - Warnings listed (do not fail build)
        - JSON output with --json flag (machine readable)
Exit codes:
    0 = success (no errors)
    1 = errors found
Warnings do not fail build.
"""
from __future__ import annotations
import re
import sys
import json
import argparse
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

documents: List[Dict[str, Any]] = []  # Flat list of all parsed entity docs with meta info

def is_kebab(name: str) -> bool:
    return bool(RE_NAME.match(name))

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

    # Annotation checks (soft warnings)
    annotations = metadata.get("annotations", {}) if isinstance(metadata.get("annotations"), dict) else {}
    if kind in {"Component", "System", "API"}:
        if "github.com/project-slug" not in annotations:
            warn(f"{kind} '{name}' missing annotation github.com/project-slug")
    if kind in {"Component", "System"}:
        if "backstage.io/techdocs-ref" not in annotations:
            warn(f"{kind} '{name}' missing annotation backstage.io/techdocs-ref")

    # Owner warnings for relevant kinds
    if kind in {"Component", "System", "Domain", "API", "Group"}:
        spec = doc.get("spec", {})
        owner = spec.get("owner")
        if not owner:
            warn(f"Kind {kind} missing spec.owner")

    # Store for relation validation later
    doc["__file__"] = str(source)
    doc["__index__"] = index + 1
    documents.append(doc)


def validate_relations() -> None:
    """Validate cross-entity references (owners, system->domain, component->system)."""
    # Build lookup maps
    by_kind_name: Dict[Tuple[str, str], Dict[str, Any]] = {}
    groups: Dict[str, Dict[str, Any]] = {}
    for doc in documents:
        kind = doc.get("kind")
        name = doc.get("metadata", {}).get("name")
        if not kind or not name:
            continue
        by_kind_name[(kind, name)] = doc
        if kind == "Group":
            groups[name] = doc

    # Validate owners
    for doc in documents:
        kind = doc.get("kind")
        spec = doc.get("spec", {})
        owner = spec.get("owner")
        if owner and isinstance(owner, str):
            if owner.startswith("group:"):
                group_name = owner.split(":", 1)[1]
                if group_name not in groups:
                    errors.append(f"{doc['__file__']} [doc {doc['__index__']}] owner references missing group '{group_name}'")
            # Could extend for user: prefix
        elif owner and not isinstance(owner, str):
            warnings.append(f"{doc['__file__']} [doc {doc['__index__']}] owner field not a string")

    # Component -> System relation
    for doc in documents:
        if doc.get("kind") == "Component":
            spec = doc.get("spec", {})
            system = spec.get("system")
            if system:
                sys_key = ("System", system)
                if sys_key not in by_kind_name:
                    errors.append(f"{doc['__file__']} [doc {doc['__index__']}] references missing System '{system}'")

    # System -> Domain relation
    for doc in documents:
        if doc.get("kind") == "System":
            spec = doc.get("spec", {})
            domain = spec.get("domain")
            if domain:
                dom_key = ("Domain", domain)
                if dom_key not in by_kind_name:
                    errors.append(f"{doc['__file__']} [doc {doc['__index__']}] references missing Domain '{domain}'")


def build_json_summary() -> Dict[str, Any]:
    return {
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
        "entities": [
            {
                "kind": d.get("kind"),
                "name": d.get("metadata", {}).get("name"),
                "file": d.get("__file__"),
                "index": d.get("__index__"),
            }
            for d in documents if d.get("kind") and d.get("metadata", {}).get("name")
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Backstage/Roadie catalog YAML")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary to stdout (suppresses human output except errors)")
    args = parser.parse_args()

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

    # Relation checks (after all docs loaded)
    validate_relations()

    if args.json:
        # Emit JSON only
        summary = build_json_summary()
        print(json.dumps(summary, indent=2))
        return 1 if errors else 0

    # Human output
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

"""Main MCP server implementation for Roadie expertise."""

import asyncio
import yaml
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from mcp.server.stdio import stdio_server

from .templates import (
    CATALOG_INFO_TEMPLATE,
    TECHDOCS_TEMPLATE,
    SCAFFOLDER_TEMPLATE,
    API_TEMPLATE,
    COMPONENT_TEMPLATES,
)


# Initialize MCP server
app = Server("roadie-mcp-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available Roadie/Backstage YAML templates."""
    return [
        Resource(
            uri="template://catalog-info",
            name="Catalog Info Template",
            mimeType="application/x-yaml",
            description="Basic catalog-info.yaml template for Backstage components",
        ),
        Resource(
            uri="template://techdocs",
            name="TechDocs Template",
            mimeType="application/x-yaml",
            description="TechDocs configuration template with MkDocs setup",
        ),
        Resource(
            uri="template://scaffolder",
            name="Scaffolder Template",
            mimeType="application/x-yaml",
            description="Software template for Backstage scaffolder",
        ),
        Resource(
            uri="template://api",
            name="API Template",
            mimeType="application/x-yaml",
            description="API definition template for Backstage",
        ),
        Resource(
            uri="template://component/service",
            name="Service Component Template",
            mimeType="application/x-yaml",
            description="Component template for microservice",
        ),
        Resource(
            uri="template://component/website",
            name="Website Component Template",
            mimeType="application/x-yaml",
            description="Component template for website",
        ),
        Resource(
            uri="template://component/library",
            name="Library Component Template",
            mimeType="application/x-yaml",
            description="Component template for library",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific template resource."""
    template_map = {
        "template://catalog-info": CATALOG_INFO_TEMPLATE,
        "template://techdocs": TECHDOCS_TEMPLATE,
        "template://scaffolder": SCAFFOLDER_TEMPLATE,
        "template://api": API_TEMPLATE,
        "template://component/service": COMPONENT_TEMPLATES["service"],
        "template://component/website": COMPONENT_TEMPLATES["website"],
        "template://component/library": COMPONENT_TEMPLATES["library"],
    }
    
    if uri not in template_map:
        raise ValueError(f"Unknown template: {uri}")
    
    return template_map[uri]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Roadie expertise tools."""
    return [
        Tool(
            name="generate_catalog_info",
            description="Generate a catalog-info.yaml file for a Backstage component",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Component name",
                    },
                    "description": {
                        "type": "string",
                        "description": "Component description",
                    },
                    "type": {
                        "type": "string",
                        "description": "Component type (service, website, library, etc.)",
                        "enum": ["service", "website", "library", "documentation", "other"],
                    },
                    "owner": {
                        "type": "string",
                        "description": "Team or user that owns this component",
                    },
                    "lifecycle": {
                        "type": "string",
                        "description": "Lifecycle stage",
                        "enum": ["experimental", "production", "deprecated"],
                        "default": "production",
                    },
                    "system": {
                        "type": "string",
                        "description": "System this component belongs to (optional)",
                    },
                },
                "required": ["name", "description", "type", "owner"],
            },
        ),
        Tool(
            name="generate_scaffolder_template",
            description="Generate a software template for Backstage Scaffolder",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Template name",
                    },
                    "description": {
                        "type": "string",
                        "description": "Template description",
                    },
                    "type": {
                        "type": "string",
                        "description": "Template type",
                        "default": "service",
                    },
                    "owner": {
                        "type": "string",
                        "description": "Team or user that owns this template",
                    },
                },
                "required": ["name", "description", "owner"],
            },
        ),
        Tool(
            name="validate_catalog_info",
            description="Validate a catalog-info.yaml file structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "yaml_content": {
                        "type": "string",
                        "description": "YAML content to validate",
                    },
                },
                "required": ["yaml_content"],
            },
        ),
        Tool(
            name="roadie_best_practices",
            description="Get Roadie/Backstage best practices and recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic for best practices",
                        "enum": [
                            "catalog",
                            "techdocs",
                            "scaffolder",
                            "plugins",
                            "organization",
                            "security",
                        ],
                    },
                },
                "required": ["topic"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Execute a Roadie expertise tool."""
    
    if name == "generate_catalog_info":
        yaml_content = generate_catalog_info(
            name=arguments["name"],
            description=arguments["description"],
            comp_type=arguments["type"],
            owner=arguments["owner"],
            lifecycle=arguments.get("lifecycle", "production"),
            system=arguments.get("system"),
        )
        return [TextContent(type="text", text=yaml_content)]
    
    elif name == "generate_scaffolder_template":
        yaml_content = generate_scaffolder_template(
            name=arguments["name"],
            description=arguments["description"],
            template_type=arguments.get("type", "service"),
            owner=arguments["owner"],
        )
        return [TextContent(type="text", text=yaml_content)]
    
    elif name == "validate_catalog_info":
        result = validate_catalog_info(arguments["yaml_content"])
        return [TextContent(type="text", text=result)]
    
    elif name == "roadie_best_practices":
        practices = get_best_practices(arguments["topic"])
        return [TextContent(type="text", text=practices)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


def generate_catalog_info(
    name: str,
    description: str,
    comp_type: str,
    owner: str,
    lifecycle: str = "production",
    system: str | None = None,
) -> str:
    """Generate a catalog-info.yaml file."""
    data = {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": name,
            "description": description,
            "annotations": {
                "github.com/project-slug": f"org/{name}",
                "backstage.io/techdocs-ref": "dir:.",
            },
            "tags": ["generated"],
        },
        "spec": {
            "type": comp_type,
            "lifecycle": lifecycle,
            "owner": owner,
        },
    }
    
    if system:
        data["spec"]["system"] = system
    
    return yaml.dump(data, sort_keys=False, default_flow_style=False)


def generate_scaffolder_template(
    name: str,
    description: str,
    template_type: str,
    owner: str,
) -> str:
    """Generate a scaffolder template."""
    data = {
        "apiVersion": "scaffolder.backstage.io/v1beta3",
        "kind": "Template",
        "metadata": {
            "name": name,
            "title": name.replace("-", " ").title(),
            "description": description,
            "tags": ["recommended", template_type],
        },
        "spec": {
            "owner": owner,
            "type": template_type,
            "parameters": [
                {
                    "title": "Provide information about the new component",
                    "required": ["component_id", "owner"],
                    "properties": {
                        "component_id": {
                            "title": "Name",
                            "type": "string",
                            "description": "Unique name of the component",
                        },
                        "description": {
                            "title": "Description",
                            "type": "string",
                            "description": "Description of the component",
                        },
                        "owner": {
                            "title": "Owner",
                            "type": "string",
                            "description": "Owner of the component",
                            "ui:field": "OwnerPicker",
                            "ui:options": {
                                "catalogFilter": {
                                    "kind": ["Group", "User"],
                                },
                            },
                        },
                    },
                },
            ],
            "steps": [
                {
                    "id": "fetch",
                    "name": "Fetch Template",
                    "action": "fetch:template",
                    "input": {
                        "url": "./template",
                        "values": {
                            "component_id": "${{ parameters.component_id }}",
                            "description": "${{ parameters.description }}",
                            "owner": "${{ parameters.owner }}",
                        },
                    },
                },
                {
                    "id": "publish",
                    "name": "Publish",
                    "action": "publish:github",
                    "input": {
                        "allowedHosts": ["github.com"],
                        "description": "This is ${{ parameters.component_id }}",
                        "repoUrl": "github.com?owner=org&repo=${{ parameters.component_id }}",
                    },
                },
                {
                    "id": "register",
                    "name": "Register",
                    "action": "catalog:register",
                    "input": {
                        "repoContentsUrl": "${{ steps.publish.output.repoContentsUrl }}",
                        "catalogInfoPath": "/catalog-info.yaml",
                    },
                },
            ],
            "output": {
                "links": [
                    {
                        "title": "Repository",
                        "url": "${{ steps.publish.output.remoteUrl }}",
                    },
                    {
                        "title": "Open in catalog",
                        "icon": "catalog",
                        "entityRef": "${{ steps.register.output.entityRef }}",
                    },
                ],
            },
        },
    }
    
    return yaml.dump(data, sort_keys=False, default_flow_style=False)


def validate_catalog_info(yaml_content: str) -> str:
    """Validate catalog-info.yaml structure."""
    try:
        data = yaml.safe_load(yaml_content)
        
        errors = []
        warnings = []
        
        # Check required fields
        if not isinstance(data, dict):
            return "❌ Invalid YAML: Root element must be an object"
        
        if "apiVersion" not in data:
            errors.append("Missing required field: apiVersion")
        elif data["apiVersion"] != "backstage.io/v1alpha1":
            warnings.append(f"Unexpected apiVersion: {data['apiVersion']}")
        
        if "kind" not in data:
            errors.append("Missing required field: kind")
        elif data["kind"] not in ["Component", "API", "Resource", "System", "Domain", "Location"]:
            warnings.append(f"Unusual kind: {data['kind']}")
        
        if "metadata" not in data:
            errors.append("Missing required field: metadata")
        else:
            metadata = data["metadata"]
            if "name" not in metadata:
                errors.append("Missing required field: metadata.name")
        
        if data.get("kind") in ["Component", "API", "Resource"]:
            if "spec" not in data:
                errors.append("Missing required field: spec")
            else:
                spec = data["spec"]
                if data["kind"] == "Component":
                    if "type" not in spec:
                        errors.append("Missing required field: spec.type")
                    if "owner" not in spec:
                        errors.append("Missing required field: spec.owner")
                    if "lifecycle" not in spec:
                        warnings.append("Recommended field missing: spec.lifecycle")
        
        # Build response
        if errors:
            return "❌ Validation failed:\n" + "\n".join(f"  • {e}" for e in errors)
        elif warnings:
            return "⚠️  Validation passed with warnings:\n" + "\n".join(f"  • {w}" for w in warnings)
        else:
            return "✅ Validation passed successfully!"
        
    except yaml.YAMLError as e:
        return f"❌ Invalid YAML syntax: {str(e)}"
    except Exception as e:
        return f"❌ Validation error: {str(e)}"


def get_best_practices(topic: str) -> str:
    """Get best practices for a specific topic."""
    practices = {
        "catalog": """
# Catalog Best Practices

## Organization
- Use meaningful component names (lowercase, hyphen-separated)
- Add comprehensive descriptions
- Tag components appropriately for discovery
- Define clear ownership (teams or users)

## Metadata
- Always include annotations for integrations (GitHub, CI/CD, etc.)
- Use consistent naming conventions across your catalog
- Document dependencies using `dependsOn` and `providesApis`

## Lifecycle Management
- Use lifecycle stages: experimental, production, deprecated
- Update lifecycle as components evolve
- Remove deprecated components after migration period

## Systems and Domains
- Group related components into systems
- Organize systems into domains for better structure
- Keep hierarchy shallow (2-3 levels max)
""",
        "techdocs": """
# TechDocs Best Practices

## Setup
- Use MkDocs with mkdocs.yml configuration
- Store docs in `/docs` directory
- Enable TechDocs annotation in catalog-info.yaml

## Content
- Write comprehensive README.md as the main page
- Use clear navigation structure
- Include API documentation and examples
- Keep documentation close to code

## Maintenance
- Update docs with code changes
- Use automated builds and publishing
- Review docs regularly for accuracy
- Enable previews for pull requests
""",
        "scaffolder": """
# Scaffolder Best Practices

## Template Design
- Create reusable, parameterized templates
- Use clear parameter names and descriptions
- Provide sensible defaults
- Use input validation

## Steps
- Keep steps simple and focused
- Use built-in actions when possible
- Provide clear step names
- Handle errors gracefully

## Output
- Always register created components
- Provide useful links (repo, catalog, docs)
- Include next steps guidance
""",
        "plugins": """
# Plugins Best Practices

## Selection
- Use official Roadie/Backstage plugins when available
- Evaluate community plugins carefully
- Consider maintenance and support

## Integration
- Configure plugins in app-config.yaml
- Provide necessary credentials securely
- Test integrations thoroughly
- Document custom plugins

## Customization
- Extend existing plugins rather than forking
- Contribute improvements back to community
- Keep customizations minimal and maintainable
""",
        "organization": """
# Organization Best Practices

## Teams and Users
- Sync teams from identity provider
- Define clear ownership boundaries
- Use group hierarchies appropriately
- Document team responsibilities

## Permissions
- Implement RBAC for sensitive operations
- Use principle of least privilege
- Audit permissions regularly
- Document access policies

## Catalog Structure
- Organize by business domains
- Use systems for technical grouping
- Keep flat structures when possible
- Avoid over-categorization
""",
        "security": """
# Security Best Practices

## Authentication
- Use SSO/SAML for authentication
- Implement MFA where required
- Rotate credentials regularly
- Use service accounts for automation

## Secrets Management
- Never commit secrets to repositories
- Use secret management tools (Vault, AWS Secrets Manager)
- Rotate secrets regularly
- Audit secret access

## Access Control
- Implement role-based access control
- Review permissions quarterly
- Use least privilege principle
- Log security events

## Integrations
- Use OAuth tokens with minimal scopes
- Rotate integration tokens regularly
- Monitor API usage
- Implement rate limiting
""",
    }
    
    return practices.get(topic, f"No best practices found for topic: {topic}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())

# Roadie MCP Server

A Model Context Protocol (MCP) server that provides Roadie/Backstage expertise and YAML templates for building internal developer portals.

## Features

### 🛠️ Tools

- **generate_catalog_info**: Generate catalog-info.yaml files for Backstage components
- **generate_scaffolder_template**: Create software templates for Backstage Scaffolder
- **validate_catalog_info**: Validate catalog-info.yaml structure and content
- **roadie_best_practices**: Get best practices for catalog, TechDocs, scaffolder, plugins, organization, and security

### 📚 Resources

Pre-built YAML templates for:
- Catalog Info (Components)
- TechDocs Configuration
- Scaffolder Templates
- API Definitions
- Component Types (Service, Website, Library)

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using uv (recommended)

```bash
uv pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python -m roadie_mcp_server.server
```

Or using the console script:

```bash
roadie-mcp-server
```

### Configuration with Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "roadie": {
      "command": "python",
      "args": [
        "-m",
        "roadie_mcp_server.server"
      ],
      "env": {}
    }
  }
}
```

Or if installed as a package:

```json
{
  "mcpServers": {
    "roadie": {
      "command": "roadie-mcp-server",
      "args": []
    }
  }
}
```

### Using with MCP Inspector

For testing and debugging:

```bash
npx @modelcontextprotocol/inspector python -m roadie_mcp_server.server
```

## Examples

### Generate a Catalog Info File

```python
# Using the generate_catalog_info tool
{
  "name": "my-service",
  "description": "My microservice",
  "type": "service",
  "owner": "backend-team",
  "lifecycle": "production",
  "system": "payment-platform"
}
```

### Validate Catalog Info

```python
# Using the validate_catalog_info tool
{
  "yaml_content": """
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
spec:
  type: service
  owner: backend-team
"""
}
```

### Get Best Practices

```python
# Using the roadie_best_practices tool
{
  "topic": "catalog"  # Options: catalog, techdocs, scaffolder, plugins, organization, security
}
```

## YAML Templates

The server provides several pre-built templates accessible as MCP resources:

- `template://catalog-info` - Basic component catalog info
- `template://techdocs` - TechDocs configuration
- `template://scaffolder` - Scaffolder template
- `template://api` - API definition
- `template://component/service` - Service component
- `template://component/website` - Website component
- `template://component/library` - Library component

## Template Examples

See the `templates/` directory for complete examples:

- `catalog-info.yaml` - Full-featured component example
- `mkdocs.yml` - TechDocs MkDocs configuration
- `scaffolder-template.yaml` - Complete scaffolder template

See the `examples/` directory for additional entity types:

- `system.yaml` - System entity
- `domain.yaml` - Domain entity
- `resource.yaml` - Resource entity
- `api.yaml` - API entity with OpenAPI spec

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/AngC1/Roadie.git
cd Roadie

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## Roadie/Backstage Resources

- [Backstage Documentation](https://backstage.io/docs/)
- [Roadie Documentation](https://roadie.io/docs/)
- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [TechDocs](https://backstage.io/docs/features/techdocs/)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
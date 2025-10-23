# Roadie MCP Server - Quick Start Guide

Get started with the Roadie MCP Server in minutes!

## Prerequisites

- Python 3.10 or higher
- pip or uv package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/AngC1/Roadie.git
cd Roadie

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
python -m roadie_mcp_server.server
```

## Using with Claude Desktop

1. Open your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the Roadie MCP server:

```json
{
  "mcpServers": {
    "roadie": {
      "command": "python",
      "args": [
        "-m",
        "roadie_mcp_server.server"
      ],
      "cwd": "/path/to/Roadie"
    }
  }
}
```

3. Restart Claude Desktop

## Quick Examples

### Generate a Component

Ask Claude:
> "Generate a catalog-info.yaml for a payment service owned by the backend team"

### Validate YAML

Ask Claude:
> "Validate this catalog-info.yaml: [paste your YAML]"

### Get Best Practices

Ask Claude:
> "What are the best practices for organizing a Backstage catalog?"

### Browse Templates

Ask Claude:
> "Show me a template for a microservice component"

## Available Tools

1. **generate_catalog_info** - Create catalog-info.yaml files
2. **generate_scaffolder_template** - Create scaffolder templates
3. **validate_catalog_info** - Validate YAML structure
4. **roadie_best_practices** - Get expert recommendations

## Available Resources

- `template://catalog-info` - Basic catalog info
- `template://techdocs` - TechDocs setup
- `template://scaffolder` - Scaffolder template
- `template://api` - API definition
- `template://component/service` - Service component
- `template://component/website` - Website component
- `template://component/library` - Library component

## Example Workflows

### Creating a New Microservice

1. Generate the catalog-info.yaml
2. Validate the structure
3. Get catalog best practices
4. Review example templates

### Setting Up TechDocs

1. Request the TechDocs template
2. Get TechDocs best practices
3. Review mkdocs.yml example

### Building a Software Template

1. Generate a scaffolder template base
2. Get scaffolder best practices
3. Review complete example

## Learn More

- [Full Usage Guide](USAGE.md) - Detailed documentation
- [README](README.md) - Complete project information
- [Backstage Docs](https://backstage.io/docs/) - Official Backstage documentation
- [Roadie Docs](https://roadie.io/docs/) - Official Roadie documentation

## Troubleshooting

**Server won't start:**
- Check Python version: `python --version` (need 3.10+)
- Verify dependencies: `pip list | grep -E "mcp|pyyaml"`

**Claude can't find the server:**
- Verify config file path is correct
- Check the `cwd` points to the Roadie directory
- Restart Claude Desktop after config changes

**Import errors:**
- Ensure you're in the Roadie directory
- Try: `python -c "import sys; sys.path.insert(0, 'src'); from roadie_mcp_server import __version__; print(__version__)"`

## Support

For issues or questions, please refer to the [full documentation](README.md) or check the [examples](examples/) directory.

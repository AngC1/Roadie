# Roadie MCP Server Usage Guide

This guide provides detailed examples of how to use the Roadie MCP Server effectively.

## Available Tools

### 1. generate_catalog_info

Generate a catalog-info.yaml file for any Backstage component.

**Parameters:**
- `name` (required): Component name (lowercase, hyphen-separated)
- `description` (required): Brief description of the component
- `type` (required): Component type - `service`, `website`, `library`, `documentation`, or `other`
- `owner` (required): Team or user that owns this component
- `lifecycle` (optional): `experimental`, `production`, or `deprecated` (default: `production`)
- `system` (optional): System this component belongs to

**Example Request:**
```json
{
  "name": "payment-service",
  "description": "Handles payment processing and transactions",
  "type": "service",
  "owner": "backend-team",
  "lifecycle": "production",
  "system": "payment-platform"
}
```

**Example Output:**
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Handles payment processing and transactions
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
  tags:
    - generated
spec:
  type: service
  lifecycle: production
  owner: backend-team
  system: payment-platform
```

### 2. generate_scaffolder_template

Create a software template for the Backstage Scaffolder.

**Parameters:**
- `name` (required): Template name
- `description` (required): Template description
- `type` (optional): Template type (default: `service`)
- `owner` (required): Team or user that owns this template

**Example Request:**
```json
{
  "name": "python-microservice",
  "description": "Create a new Python microservice with FastAPI",
  "type": "service",
  "owner": "platform-team"
}
```

### 3. validate_catalog_info

Validate the structure and content of a catalog-info.yaml file.

**Parameters:**
- `yaml_content` (required): The YAML content to validate

**Example Request:**
```json
{
  "yaml_content": "apiVersion: backstage.io/v1alpha1\nkind: Component\nmetadata:\n  name: my-service\nspec:\n  type: service\n  owner: backend-team"
}
```

**Example Outputs:**

✅ Valid:
```
✅ Validation passed successfully!
```

⚠️ With warnings:
```
⚠️  Validation passed with warnings:
  • Recommended field missing: spec.lifecycle
```

❌ Invalid:
```
❌ Validation failed:
  • Missing required field: spec.owner
  • Missing required field: metadata.name
```

### 4. roadie_best_practices

Get best practices and recommendations for various Backstage/Roadie topics.

**Parameters:**
- `topic` (required): One of `catalog`, `techdocs`, `scaffolder`, `plugins`, `organization`, or `security`

**Example Request:**
```json
{
  "topic": "catalog"
}
```

**Topics:**

- **catalog**: Best practices for organizing and maintaining the software catalog
- **techdocs**: Documentation best practices with TechDocs
- **scaffolder**: Creating effective software templates
- **plugins**: Plugin selection and integration
- **organization**: Team and user organization
- **security**: Security best practices for authentication, secrets, and access control

## Available Resources

The server provides pre-built YAML templates as MCP resources:

### Basic Templates

1. **template://catalog-info**
   - Basic catalog-info.yaml structure
   - Use as starting point for any component

2. **template://techdocs**
   - TechDocs configuration with MkDocs
   - Includes directory structure recommendations

3. **template://scaffolder**
   - Complete scaffolder template example
   - Shows parameters, steps, and output configuration

4. **template://api**
   - API definition with OpenAPI spec
   - REST API example structure

### Component Type Templates

5. **template://component/service**
   - Microservice component with common annotations
   - Includes API definitions and dependencies

6. **template://component/website**
   - Frontend/website component
   - Includes Lighthouse integration

7. **template://component/library**
   - Shared library component
   - NPM package integration example

## Common Workflows

### Creating a New Service

1. **Generate the catalog-info.yaml:**
```json
{
  "tool": "generate_catalog_info",
  "arguments": {
    "name": "user-service",
    "description": "User management and authentication service",
    "type": "service",
    "owner": "identity-team",
    "lifecycle": "production",
    "system": "identity-platform"
  }
}
```

2. **Validate the output:**
```json
{
  "tool": "validate_catalog_info",
  "arguments": {
    "yaml_content": "<generated yaml from step 1>"
  }
}
```

3. **Get best practices:**
```json
{
  "tool": "roadie_best_practices",
  "arguments": {
    "topic": "catalog"
  }
}
```

### Setting up TechDocs

1. **Get TechDocs template:**
   - Access resource: `template://techdocs`

2. **Get best practices:**
```json
{
  "tool": "roadie_best_practices",
  "arguments": {
    "topic": "techdocs"
  }
}
```

### Creating a Scaffolder Template

1. **Generate base template:**
```json
{
  "tool": "generate_scaffolder_template",
  "arguments": {
    "name": "react-app-template",
    "description": "Create a new React application with TypeScript",
    "type": "website",
    "owner": "frontend-team"
  }
}
```

2. **Get scaffolder best practices:**
```json
{
  "tool": "roadie_best_practices",
  "arguments": {
    "topic": "scaffolder"
  }
}
```

## Tips and Best Practices

### Component Naming
- Use lowercase with hyphens: `user-service`, `payment-api`
- Be descriptive but concise
- Avoid redundant suffixes like `-component` or `-app`

### Ownership
- Always specify a team or group as owner
- Ensure owners exist in your Backstage catalog
- Use consistent team naming across components

### Lifecycle Management
- Start with `experimental` for new services
- Move to `production` when stable
- Mark as `deprecated` before removal
- Document migration paths for deprecated services

### Systems and Domains
- Group related components into systems
- Use systems to show component relationships
- Create domains for business area organization
- Keep hierarchy simple (2-3 levels maximum)

### Tags
- Use tags for discovery and filtering
- Include technology tags: `nodejs`, `python`, `react`
- Add functional tags: `api`, `database`, `frontend`
- Keep tags consistent across similar components

### Annotations
- Always include source repository annotation
- Add CI/CD integration annotations
- Include monitoring and alerting integrations
- Link to deployment dashboards

## Troubleshooting

### Validation Errors

**Missing required fields:**
- Ensure `apiVersion`, `kind`, and `metadata.name` are present
- Check `spec.type` and `spec.owner` for Components

**YAML syntax errors:**
- Use proper indentation (2 or 4 spaces, consistent)
- Quote strings with special characters
- Validate YAML with online tools if needed

### Integration Issues

**Component not appearing in catalog:**
- Check catalog-info.yaml is in repository root
- Verify repository is registered in Backstage
- Check for validation errors in Backstage UI
- Ensure owner exists in catalog

**TechDocs not building:**
- Verify mkdocs.yml exists in repository
- Check TechDocs annotation in catalog-info.yaml
- Ensure docs directory exists with index.md
- Review build logs for errors

## Advanced Usage

### Multi-Entity Files

You can define multiple entities in a single YAML file:

```yaml
---
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: my-platform
spec:
  owner: platform-team
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
spec:
  type: service
  owner: platform-team
  system: my-platform
```

### Entity Relationships

Define relationships between entities:

```yaml
spec:
  # This component depends on other components
  dependsOn:
    - component:auth-service
    - resource:database
  
  # This component provides APIs
  providesApis:
    - my-api
  
  # This component consumes APIs
  consumesApis:
    - auth-api
    - payment-api
  
  # This is a subcomponent of another component
  subcomponentOf: component:platform
```

### Custom Annotations

Add custom annotations for integrations:

```yaml
metadata:
  annotations:
    # Source control
    github.com/project-slug: org/repo
    
    # CI/CD
    circleci.com/project-slug: github/org/repo
    jenkins.io/job-full-name: folder/job
    
    # Monitoring
    pagerduty.com/integration-key: <key>
    grafana/dashboard-selector: tag:service
    
    # Documentation
    backstage.io/techdocs-ref: dir:.
    
    # Cloud resources
    aws.com/lambda-function-name: my-function
    cloud.google.com/project-id: my-project
```

## Resources

- [Backstage Documentation](https://backstage.io/docs/)
- [Roadie Documentation](https://roadie.io/docs/)
- [Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [TechDocs](https://backstage.io/docs/features/techdocs/)
- [Scaffolder](https://backstage.io/docs/features/software-templates/)

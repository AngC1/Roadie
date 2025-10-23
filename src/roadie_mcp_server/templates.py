"""YAML templates for Roadie/Backstage components."""

CATALOG_INFO_TEMPLATE = """apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-component
  description: A description of my component
  annotations:
    github.com/project-slug: org/my-component
    backstage.io/techdocs-ref: dir:.
  tags:
    - typescript
    - react
spec:
  type: service
  lifecycle: production
  owner: team-name
  system: my-system
  providesApis:
    - my-api
  consumesApis:
    - external-api
"""

TECHDOCS_TEMPLATE = """# TechDocs Configuration

## mkdocs.yml
site_name: My Component Documentation
site_description: Documentation for my component

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference: api.md
  - Contributing: contributing.md

plugins:
  - techdocs-core

## catalog-info.yaml annotation
metadata:
  annotations:
    backstage.io/techdocs-ref: dir:.

## Directory structure
docs/
  index.md
  getting-started.md
  api.md
  contributing.md
mkdocs.yml
"""

SCAFFOLDER_TEMPLATE = """apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: create-react-app-template
  title: Create React App
  description: Create a new React application
  tags:
    - recommended
    - react
    - typescript
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Provide information about the new component
      required:
        - component_id
        - owner
      properties:
        component_id:
          title: Name
          type: string
          description: Unique name of the component
          ui:field: EntityNamePicker
        description:
          title: Description
          type: string
          description: Help others understand what this component does
        owner:
          title: Owner
          type: string
          description: Owner of the component
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind:
                - Group
                - User

    - title: Choose a location
      required:
        - repoUrl
      properties:
        repoUrl:
          title: Repository Location
          type: string
          ui:field: RepoUrlPicker
          ui:options:
            allowedHosts:
              - github.com

  steps:
    - id: fetch-base
      name: Fetch Base
      action: fetch:template
      input:
        url: ./template
        values:
          component_id: ${{ parameters.component_id }}
          description: ${{ parameters.description }}
          owner: ${{ parameters.owner }}
          destination: ${{ parameters.repoUrl | parseRepoUrl }}

    - id: publish
      name: Publish
      action: publish:github
      input:
        allowedHosts:
          - github.com
        description: This is ${{ parameters.component_id }}
        repoUrl: ${{ parameters.repoUrl }}

    - id: register
      name: Register
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Open in catalog
        icon: catalog
        entityRef: ${{ steps.register.output.entityRef }}
"""

API_TEMPLATE = """apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: my-api
  description: The My API
  tags:
    - rest
    - openapi
spec:
  type: openapi
  lifecycle: production
  owner: team-name
  system: my-system
  definition: |
    openapi: 3.0.0
    info:
      title: My API
      version: 1.0.0
      description: API for my service
    paths:
      /health:
        get:
          summary: Health check
          responses:
            '200':
              description: Service is healthy
      /api/v1/items:
        get:
          summary: List items
          responses:
            '200':
              description: List of items
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      type: object
"""

COMPONENT_TEMPLATES = {
    "service": """apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  description: A microservice component
  annotations:
    github.com/project-slug: org/my-service
    backstage.io/techdocs-ref: dir:.
    pagerduty.com/integration-key: <integration-key>
  tags:
    - microservice
    - api
  links:
    - url: https://dashboard.example.com
      title: Dashboard
      icon: dashboard
spec:
  type: service
  lifecycle: production
  owner: backend-team
  system: backend-platform
  providesApis:
    - my-service-api
  dependsOn:
    - resource:database
    - component:auth-service
""",
    "website": """apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-website
  description: A website/frontend component
  annotations:
    github.com/project-slug: org/my-website
    backstage.io/techdocs-ref: dir:.
    lighthouse.com/website-url: https://example.com
  tags:
    - frontend
    - react
    - typescript
  links:
    - url: https://example.com
      title: Production
      icon: web
    - url: https://staging.example.com
      title: Staging
      icon: web
spec:
  type: website
  lifecycle: production
  owner: frontend-team
  system: customer-portal
  consumesApis:
    - backend-api
    - auth-api
""",
    "library": """apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-library
  description: A shared library component
  annotations:
    github.com/project-slug: org/my-library
    backstage.io/techdocs-ref: dir:.
    npm.com/package-name: @myorg/my-library
  tags:
    - library
    - shared
    - typescript
  links:
    - url: https://www.npmjs.com/package/@myorg/my-library
      title: NPM Package
      icon: code
spec:
  type: library
  lifecycle: production
  owner: platform-team
  system: shared-libraries
  subcomponentOf: component:design-system
""",
}

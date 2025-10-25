# Scaffolder Templates

This directory contains Backstage Software Templates (scaffolders) for the Eulen platform.

## Available Templates

### 1. Angular Component Template
**File**: `angular-component.yaml`

Creates a new Angular frontend component with:
- Angular 17+ setup
- TypeScript configuration
- Basic component structure
- Catalog registration

**Use when**: Creating new frontend applications or micro-frontends.

### 2. Node.js Express API Template
**File**: `nodejs-api.yaml`

Creates a new Node.js/Express REST API with:
- Express.js setup
- CORS and Helmet security
- OpenAPI specification
- Health check endpoint
- Catalog registration with API entity

**Use when**: Creating new backend REST APIs.

### 3. Spring Boot Service Template
**File**: `spring-boot-service.yaml`

Creates a new Spring Boot microservice with:
- Spring Boot 3.2+ setup
- Maven configuration
- Spring Actuator for monitoring
- Java 17 or 21
- Catalog registration

**Use when**: Creating new Java microservices.

## How to Use

1. **In Roadie**, navigate to: Create → Choose a template
2. Select one of the templates above
3. Fill in the required information:
   - Component name
   - Description
   - Owner team
   - Repository location
4. Click **Create**
5. Roadie will:
   - Generate the code from the skeleton
   - Create a new GitHub repository
   - Register the component in the catalog

## Template Structure

Each template consists of:
- `<template-name>.yaml` - Template definition with parameters and steps
- `skeleton/<template-name>/` - Template files with variable placeholders

## Variables

Templates use Nunjucks syntax for variables:
- `${{ values.name }}` - Component name
- `${{ values.description }}` - Component description
- `${{ values.owner }}` - Owner team
- `${{ values.destination }}` - Repository information

## Customization

To customize templates:
1. Edit the YAML file to add/remove parameters
2. Modify skeleton files to change generated code
3. Commit and push changes
4. Templates update automatically in Roadie

## System Integration

All templates create components that:
- Belong to the `eulen-platform` system
- Are owned by appropriate teams (frontend/backend)
- Include proper catalog metadata
- Follow Eulen platform conventions

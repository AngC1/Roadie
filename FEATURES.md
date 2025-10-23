# Roadie MCP Server Features

## 🎯 What is this?

The Roadie MCP Server is an AI-powered assistant that provides expert knowledge about **Roadie** and **Backstage** (internal developer portals). It helps you:

- Generate YAML configuration files
- Create software templates
- Validate catalog entries
- Get best practices and recommendations
- Access pre-built templates for common patterns

## 🛠️ Tools Available

### 1. Generate Catalog Info
**Purpose**: Create a `catalog-info.yaml` file for any component

**Use when**:
- Adding a new service to your catalog
- Documenting an existing component
- Creating API or resource definitions

**Example**:
```
Generate a catalog-info.yaml for:
- Name: user-service
- Type: microservice
- Owner: backend-team
- Lifecycle: production
```

**Output**: Complete, valid YAML file ready to use

---

### 2. Generate Scaffolder Template
**Purpose**: Create a software template for the Backstage Scaffolder

**Use when**:
- Building a template for creating new projects
- Standardizing project setup
- Automating repository creation

**Example**:
```
Create a scaffolder template for:
- Python microservices
- With FastAPI framework
- Owned by platform-team
```

**Output**: Complete scaffolder template with parameters and steps

---

### 3. Validate Catalog Info
**Purpose**: Check if your catalog-info.yaml is valid

**Use when**:
- Before committing changes
- Debugging catalog issues
- Ensuring best practices

**Example**:
```
Validate this catalog-info.yaml:
[paste your YAML]
```

**Output**: ✅ Valid / ⚠️ Warnings / ❌ Errors with specific feedback

---

### 4. Get Best Practices
**Purpose**: Expert recommendations for Roadie/Backstage

**Topics Available**:
- **catalog**: Organizing and maintaining your software catalog
- **techdocs**: Documentation best practices
- **scaffolder**: Creating effective templates
- **plugins**: Plugin selection and integration
- **organization**: Team and user management
- **security**: Authentication, secrets, and access control

**Example**:
```
What are the best practices for:
- Organizing a Backstage catalog?
- Setting up TechDocs?
- Creating scaffolder templates?
```

**Output**: Detailed recommendations and guidelines

---

## 📚 Template Resources

Pre-built YAML templates you can access:

| Template | Description | Use Case |
|----------|-------------|----------|
| **catalog-info** | Basic component structure | Any component registration |
| **techdocs** | Documentation setup | Setting up TechDocs |
| **scaffolder** | Software template | Creating project templates |
| **api** | API definition | Documenting APIs |
| **component/service** | Microservice | Backend services |
| **component/website** | Frontend app | Web applications |
| **component/library** | Shared code | Libraries and packages |

---

## 💡 Common Use Cases

### Starting a New Project
1. Generate catalog-info.yaml for your project
2. Get catalog best practices
3. Set up TechDocs (get template + best practices)
4. Validate your configuration

### Building Developer Experience
1. Create scaffolder templates for common project types
2. Get scaffolder best practices
3. Review example templates
4. Implement and test templates

### Maintaining Your Catalog
1. Validate existing catalog entries
2. Review catalog best practices
3. Update outdated components
4. Organize with systems and domains

### Improving Documentation
1. Get TechDocs template
2. Learn TechDocs best practices
3. Set up mkdocs.yml
4. Create comprehensive docs

---

## 🚀 Quick Start Examples

### Example 1: Create a Payment Service Entry
**You ask**:
> "Create a catalog-info.yaml for a payment processing service owned by the payments team in the commerce platform"

**Server provides**: Complete YAML with proper structure, annotations, and metadata

### Example 2: Validate Configuration
**You ask**:
> "Is this catalog-info.yaml valid? [paste YAML]"

**Server provides**: Validation results with specific errors or warnings

### Example 3: Learn Best Practices
**You ask**:
> "What are the security best practices for Backstage?"

**Server provides**: Comprehensive guide on authentication, secrets, access control, etc.

### Example 4: Get a Template
**You ask**:
> "Show me an example of a website component catalog-info.yaml"

**Server provides**: Pre-built template with common annotations and configurations

---

## 🎓 Learning Path

### Beginner
1. **Start with basics**: Generate a simple catalog-info.yaml
2. **Validate it**: Use the validation tool
3. **Learn catalog practices**: Get catalog best practices

### Intermediate
1. **Add TechDocs**: Get template and set it up
2. **Create relationships**: Link components with systems/APIs
3. **Learn organization**: Get organization best practices

### Advanced
1. **Build templates**: Create scaffolder templates
2. **Security hardening**: Review security practices
3. **Plugin integration**: Learn about plugin best practices

---

## 📖 Entity Types Supported

The server provides knowledge about all Backstage entity types:

| Entity | What it is | Example |
|--------|-----------|---------|
| **Component** | Software (service, website, library) | Your microservices |
| **API** | Interface definition | REST API, GraphQL |
| **Resource** | Infrastructure | Database, queue, storage |
| **System** | Collection of components | Payment platform |
| **Domain** | Business area | E-commerce, Identity |
| **Group** | Team or department | Backend team |
| **User** | Individual person | Developers |
| **Location** | External catalog reference | Git repository |

---

## 🔍 What Makes This Useful?

### For Developers
- Quick YAML generation (no manual writing)
- Instant validation (catch errors early)
- Best practices guidance (learn as you build)

### For Platform Teams
- Template standardization (consistent patterns)
- Documentation examples (less questions)
- Security guidelines (build it right)

### For Everyone
- Time savings (automated generation)
- Error reduction (validation built-in)
- Knowledge transfer (best practices included)

---

## 🤝 Integration

Works seamlessly with:
- **Claude Desktop** (via MCP protocol)
- **VS Code** (via MCP extensions)
- **Command line** (standalone server)
- **Any MCP client** (standard protocol)

---

## 📦 What You Get

✅ **4 Expert Tools** for generation, validation, and guidance  
✅ **7 Pre-built Templates** for common patterns  
✅ **6 Entity Examples** covering all types  
✅ **Comprehensive Documentation** with examples  
✅ **Best Practices** across 6 key areas  
✅ **Production Ready** code with security scanning  

---

## 🌟 Why Use This?

Instead of:
- 📖 Reading through documentation
- 🔍 Searching for examples
- ✍️ Writing YAML manually
- ❓ Guessing at best practices
- 🐛 Debugging validation errors

You get:
- 🤖 AI-powered assistance
- ⚡ Instant generation
- ✅ Built-in validation
- 💡 Expert guidance
- 🎯 Production-ready output

---

Ready to get started? Check out the [QUICKSTART.md](QUICKSTART.md) guide!

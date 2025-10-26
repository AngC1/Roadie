# Configuración de Dominios en Roadie

Los **Dominios** en Backstage/Roadie son una forma de organizar sistemas y componentes en agrupaciones lógicas de alto nivel, representando áreas de negocio o responsabilidad.

## 🎯 ¿Qué son los Dominios?

Los dominios permiten:
- **Organizar** sistemas por área de negocio o función
- **Visualizar** la arquitectura de alto nivel en Roadie
- **Navegar** por la estructura organizacional en `/explore/domains`
- **Gestionar** ownership a nivel de dominio

## 📁 Jerarquía de Entidades

```
Domain (Dominio de negocio)
└── System (Sistema técnico)
    └── Component (Componente individual)
```

**Ejemplo**:
```
frontend-domain
└── eulen-platform
    ├── eulen-portal
    └── eulen-frontend
```

## 🏗️ Dominios Creados para Eulen

### 1. **eulen-platform-domain**
- **Descripción**: Dominio principal de la Plataforma Eulen
- **Owner**: team-eulen
- **Incluye**: Sistema eulen-platform completo
- **Tags**: platform, eulen

### 2. **frontend-domain**
- **Descripción**: Aplicaciones frontend y UX
- **Owner**: team-eulen-frontend
- **Propósito**: Agrupar todos los componentes de interfaz
- **Tags**: frontend, ui, ux

### 3. **backend-domain**
- **Descripción**: Servicios backend y APIs
- **Owner**: team-eulen-backend
- **Propósito**: Microservicios y APIs REST
- **Tags**: backend, api, microservices

### 4. **data-domain**
- **Descripción**: Datos, analytics y procesamiento
- **Owner**: team-eulen-backend
- **Propósito**: ETL, analytics, data lakes
- **Tags**: data, analytics, processing

### 5. **infrastructure-domain**
- **Descripción**: Infraestructura y DevOps
- **Owner**: engineering
- **Propósito**: CI/CD, monitoring, cloud resources
- **Tags**: infrastructure, devops, platform

## 📝 Estructura de un Dominio

```yaml
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: nombre-del-dominio
  description: Descripción del dominio
  tags:
    - tag1
    - tag2
  annotations:
    github.com/project-slug: AngC1/Roadie
spec:
  owner: group:nombre-del-equipo
```

## 🔗 Asociar Sistemas a Dominios

Para que un sistema pertenezca a un dominio:

```yaml
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: mi-sistema
spec:
  owner: group:mi-equipo
  domain: nombre-del-dominio  # ← Referencia al dominio
```

## 🎨 Visualización en Roadie

### En `/explore/domains`:
1. **Vista de Dominios**: Todos los dominios como tarjetas
2. **Click en dominio**: Ver sistemas y componentes dentro
3. **Gráfico de relaciones**: Visualización de la jerarquía
4. **Ownership**: Quién es responsable de cada dominio

### Beneficios:
- ✅ Navegación intuitiva por la arquitectura
- ✅ Vista de alto nivel del portafolio
- ✅ Identificación rápida de áreas de negocio
- ✅ Ownership claro a nivel organizacional

## 🚀 Cómo Añadir un Nuevo Dominio

### Opción 1: Con GitHub Copilot

**Prompt**:
```
Añade un nuevo dominio en catalog/domains.yaml llamado "security-domain" 
de tipo Domain, descripción "Dominio de seguridad y compliance", 
owner "engineering", tags: security, compliance, governance
```

### Opción 2: Manual

1. **Edita** `catalog/domains.yaml`:
```yaml
---
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: nuevo-dominio
  description: Descripción del nuevo dominio
  tags:
    - tag-relevante
spec:
  owner: group:equipo-propietario
```

2. **Commit y push**:
```bash
git add catalog/domains.yaml
git commit -m "feat(domains): add nuevo-dominio"
git push origin main
```

3. **Espera** 1-2 minutos para que Roadie refresque

## 🔧 Asociar Componentes a Dominios

Los componentes se asocian indirectamente vía sistemas:

```
Component → System → Domain
```

**No es posible** asignar un componente directamente a un dominio. Debe hacerse a través del sistema.

## 📊 Casos de Uso

### Organización por Área de Negocio
```
sales-domain → sales-platform → [sales-crm, sales-portal]
finance-domain → finance-platform → [billing-api, invoicing-service]
```

### Organización por Tecnología
```
web-domain → web-apps → [react-app, angular-app]
mobile-domain → mobile-apps → [ios-app, android-app]
```

### Organización por Función
```
customer-facing-domain → customer-systems → [website, mobile-app, support-portal]
internal-domain → internal-systems → [admin-panel, reporting-tool]
```

## 🎯 Mejores Prácticas

### 1. Nomenclatura
- Nombres: `kebab-case` terminados en `-domain`
- Descriptivos pero concisos
- Evitar acrónimos oscuros

### 2. Granularidad
- **Muy pocos dominios**: Dificulta organización
- **Demasiados dominios**: Confusión
- **Ideal**: 5-10 dominios principales

### 3. Ownership
- Cada dominio debe tener un owner claro
- Preferir grupos sobre usuarios individuales
- Owner debe tener autoridad sobre el área

### 4. Documentación
- Descripción clara del propósito
- Tags relevantes para búsqueda
- Mantener alineado con arquitectura real

## 🔍 Consultas en Roadie

### API MCP para Dominios

Si usas el MCP server de Roadie:

```json
{
  "servers": {
    "roadie-catalog": {
      "url": "https://api.roadie.so/api/mcp/v1/rich-catalog-entity",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```

**Query**:
```javascript
// Obtener todos los dominios
GET /api/catalog/entities?filter=kind=Domain

// Obtener sistemas de un dominio
GET /api/catalog/entities?filter=kind=System,spec.domain=frontend-domain
```

## 📈 Evolución de Dominios

### Añadir Nuevo Dominio
1. Crear en `domains.yaml`
2. Asociar sistemas existentes o nuevos
3. Actualizar documentación

### Refactorizar Dominios
1. Mover sistemas entre dominios (cambiar `spec.domain`)
2. Renombrar dominio (requiere actualizar referencias)
3. Eliminar dominio (primero quitar de sistemas)

### Subdominios
Backstage no soporta subdominios nativamente. Alternativas:
- Usar naming convention: `parent-subdomain`
- Usar tags para agrupar
- Usar sistemas para jerarquía adicional

## 🛠️ Troubleshooting

### Dominio no aparece en `/explore/domains`
- Verificar que esté en `catalog-info.yaml` targets
- Esperar refresh de catálogo (1-2 min)
- Verificar sintaxis YAML
- Revisar que `kind: Domain` esté correcto

### Sistema no aparece en dominio
- Verificar `spec.domain` en el sistema
- Nombre debe coincidir exactamente
- Verificar ownership y permisos

### Error de validación
- Dominio require `spec.owner`
- Owner debe existir (grupo o usuario)
- Nombre debe ser único

## 📚 Recursos

- [Backstage System Model](https://backstage.io/docs/features/software-catalog/system-model)
- [Domain Entity](https://backstage.io/docs/features/software-catalog/descriptor-format#kind-domain)
- [Roadie Domains Guide](https://roadie.io/docs/getting-started/domains/)

## 🎓 Ejemplo Completo

```yaml
# Dominio
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: ecommerce-domain
spec:
  owner: group:ecommerce-team
---
# Sistema en el dominio
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: shop-system
spec:
  owner: group:ecommerce-team
  domain: ecommerce-domain
---
# Componente en el sistema (y por tanto en el dominio)
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: product-catalog
spec:
  type: service
  owner: group:ecommerce-team
  system: shop-system
```

**Resultado en Roadie**:
```
ecommerce-domain/
└── shop-system/
    └── product-catalog
```

---

**Archivo**: `catalog/domains.yaml`  
**Registrado en**: `catalog-info.yaml`  
**Visible en**: https://ayesa.roadie.so/explore/domains

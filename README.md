# Roadie Backstage Catalog - Eulen Platform

Este repositorio contiene el catálogo completo de Backstage para la plataforma Eulen en Roadie.io, incluyendo componentes, sistemas, grupos y templates de software.

## 📋 Índice

- [Arquitectura del Catálogo](#arquitectura-del-catálogo)
- [Componentes Principales](#componentes-principales)
- [Actualización con GitHub Copilot](#actualización-con-github-copilot)
- [Buenas Prácticas](#buenas-prácticas)
- [Software Templates (Scaffolders)](#software-templates-scaffolders)
- [Estructura de Archivos](#estructura-de-archivos)

## 🏗️ Arquitectura del Catálogo

### Archivo Raíz: `catalog-info.yaml`

El archivo `catalog-info.yaml` en la raíz es de tipo **Location** y funciona como **agregador maestro** que registra todas las entidades del catálogo:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: eulen-components
spec:
  targets:
    - ./catalog/catalog-info.yaml           # Portal principal
    - ./catalog/eulen-frontend-catalog.yaml # Frontend Angular
    - ./catalog/eulen-api-catalog.yaml      # API Node.js
    - ./catalog/eulen-spring-catalog.yaml   # Servicio Spring Boot
    - ./catalog/eulen-api.yaml              # Definición API
    - ./catalog/eulen-system.yaml           # Sistema eulen-platform
    - ./catalog/groups.yaml                 # Equipos y organizaciones
    - ./scaffolder-templates/*.yaml         # Templates de software
```

### Funcionalidad

1. **Descubrimiento Automático**: Roadie lee este archivo y automáticamente descubre todas las entidades referenciadas
2. **Gestión Centralizada**: Un único punto de entrada para todo el catálogo
3. **Organización Modular**: Cada componente tiene su propio archivo independiente
4. **Versionamiento**: Todo bajo control de versiones en Git

## 🧩 Componentes Principales

### Sistema: eulen-platform

Sistema general que agrupa todos los componentes de la plataforma Eulen.

**Archivo**: `catalog/eulen-system.yaml`

```yaml
kind: System
metadata:
  name: eulen-platform
spec:
  owner: group:team-eulen
```

### Componentes

#### 1. Eulen Portal (`eulen-portal`)
- **Tipo**: Website
- **Propietario**: team-eulen
- **Descripción**: Portal principal de la aplicación
- **Archivo**: `catalog/catalog-info.yaml`

#### 2. Eulen Frontend (`eulen-frontend`)
- **Tipo**: Frontend
- **Tecnología**: Angular 17+
- **Propietario**: team-eulen-frontend
- **Dependencias**: eulen-api
- **Archivo**: `catalog/eulen-frontend-catalog.yaml`

#### 3. Eulen API (`eulen-api`)
- **Tipo**: Service
- **Tecnología**: Node.js/Express
- **Propietario**: team-eulen-backend
- **Provee**: eulen-rest-api
- **Archivo**: `catalog/eulen-api-catalog.yaml`

#### 4. Eulen Spring (`eulen-spring`)
- **Tipo**: Service
- **Tecnología**: Spring Boot
- **Propietario**: team-eulen-backend
- **Dependencias**: eulen-api
- **Archivo**: `catalog/eulen-spring-catalog.yaml`

### API: eulen-rest-api

Definición OpenAPI del servicio REST.

**Archivo**: `catalog/eulen-api.yaml`
**Especificación**: `catalog/openapi.yaml`

### Grupos y Equipos

**Archivo**: `catalog/groups.yaml`

Estructura jerárquica:

```
engineering (organización)
└── team-eulen (equipo)
    ├── team-eulen-frontend (equipo)
    └── team-eulen-backend (equipo)
```

## 🤖 Actualización con GitHub Copilot

### Uso de Copilot para Gestionar el Catálogo

#### 1. Añadir un Nuevo Componente

**Prompt para Copilot**:
```
Añade un nuevo componente al catálogo de Backstage en catalog/ llamado "eulen-mobile" 
de tipo "frontend" usando React Native, propiedad de "team-eulen-frontend", 
que depende de "eulen-api" y pertenece al sistema "eulen-platform"
```

**Copilot creará**:
- Archivo `catalog/eulen-mobile-catalog.yaml`
- Actualizará `catalog-info.yaml` para incluirlo en targets

#### 2. Crear un Nuevo Template

**Prompt para Copilot**:
```
Crea un software template de Backstage para un microservicio Python FastAPI 
en scaffolder-templates/ con skeleton incluyendo requirements.txt, Dockerfile, 
main.py y catalog-info.yaml. Owner: team-eulen-backend
```

#### 3. Actualizar Grupos

**Prompt para Copilot**:
```
Añade un nuevo grupo "team-eulen-devops" como hijo de "team-eulen" 
en catalog/groups.yaml con la propiedad children vacía
```

#### 4. Modificar Anotaciones

**Prompt para Copilot**:
```
Añade anotaciones de GitHub Actions workflow "ci.yml" y SonarQube project key 
"eulen-api" al componente eulen-api-catalog.yaml
```

### Comandos Útiles con Copilot

**Validar sintaxis YAML**:
```
@workspace valida la sintaxis de todos los archivos catalog/*.yaml 
y verifica que tengan apiVersion, kind y metadata requeridos
```

**Generar documentación**:
```
@workspace genera un README.md en catalog/ documentando cada componente, 
su propósito, dependencias y propietarios
```

**Refactorizar**:
```
@workspace refactoriza catalog-info.yaml para organizar los targets 
por tipo (componentes, sistemas, grupos, templates)
```

## ✅ Buenas Prácticas

### 1. Estructura de Archivos

```
✅ CORRECTO:
catalog-info.yaml                    # Location (raíz)
catalog/
  ├── catalog-info.yaml             # Component
  ├── eulen-api-catalog.yaml        # Component
  ├── eulen-system.yaml             # System
  └── groups.yaml                   # Groups

❌ INCORRECTO:
catalog-info.yaml                    # Component (no Location)
components.yaml                      # Todo mezclado
```

### 2. Nomenclatura

**Componentes**:
- Nombres: `kebab-case` (eulen-frontend, eulen-api)
- Archivos: `{nombre}-catalog.yaml` o `catalog-info.yaml`

**Sistemas**:
- Nombres: `{plataforma}-platform` (eulen-platform)
- Archivos: `{nombre}-system.yaml`

**Grupos**:
- Nombres: `team-{área}` (team-eulen-frontend)
- Prefijos: `group:` en referencias (owner: group:team-eulen)

### 3. Propiedades Requeridas

**Todos los archivos deben tener**:
```yaml
apiVersion: backstage.io/v1alpha1
kind: [Component|System|Group|API|Template]
metadata:
  name: nombre-unico
  description: Descripción clara
spec:
  # Propiedades específicas del kind
```

**Groups requieren**:
```yaml
spec:
  type: [team|organization]
  children: []  # SIEMPRE incluir, aunque esté vacío
```

### 4. Anotaciones Recomendadas

```yaml
annotations:
  # GitHub
  github.com/project-slug: AngC1/Roadie
  
  # Roadie
  roadie.io/enabled: 'true'
  
  # Ubicación código fuente
  backstage.io/source-location: url:https://github.com/AngC1/Roadie
  backstage.io/view-url: https://github.com/AngC1/Roadie/tree/main/src
  backstage.io/edit-url: https://github.com/AngC1/Roadie/edit/main/src
  
  # Gestión
  backstage.io/managed-by-location: file:catalog/nombre.yaml
  backstage.io/managed-by-origin-location: file:catalog-info.yaml
  
  # TechDocs
  backstage.io/techdocs-ref: dir:.
```

### 5. Dependencias y Relaciones

**Dependencias entre componentes**:
```yaml
spec:
  dependsOn:
    - component:eulen-api
    - resource:database
```

**Provisión de APIs**:
```yaml
spec:
  providesApis:
    - eulen-rest-api
```

**Consumo de APIs**:
```yaml
spec:
  consumesApis:
    - eulen-rest-api
```

### 6. Ciclo de Vida

Usa valores estándar:
- `experimental` - En desarrollo inicial
- `production` - En producción
- `deprecated` - Marcado para eliminación

### 7. Versionamiento

**Commits semánticos**:
```bash
git commit -m "feat(catalog): add eulen-mobile component"
git commit -m "fix(groups): add required children property"
git commit -m "docs(catalog): update component descriptions"
```

### 8. Validación antes de Commit

**Con GitHub Copilot**:
```
@workspace verifica que todos los archivos en catalog/ y scaffolder-templates/ 
tengan la estructura correcta de Backstage y no falten propiedades requeridas
```

**Manual**:
```bash
# Validar YAML
yamllint catalog/*.yaml

# Probar en Roadie
# 1. Push a rama feature
# 2. Probar import en Roadie
# 3. Si funciona, merge a main
```

## 🎨 Software Templates (Scaffolders)

Los templates permiten crear nuevos componentes desde Roadie UI.

### Templates Disponibles

1. **Angular Component** (`scaffolder-templates/angular-component.yaml`)
2. **Node.js Express API** (`scaffolder-templates/nodejs-api.yaml`)
3. **Spring Boot Service** (`scaffolder-templates/spring-boot-service.yaml`)

### Crear un Nuevo Template con Copilot

**Prompt**:
```
Crea un software template de Backstage en scaffolder-templates/ para una 
aplicación Python Django con PostgreSQL. Incluye:
- Template YAML con parámetros (nombre, descripción, owner, versión Python)
- Skeleton con: manage.py, settings.py, requirements.txt, Dockerfile
- catalog-info.yaml que se registre automáticamente
- README con instrucciones de setup
```

## 📁 Estructura de Archivos Completa

```
Roadie/
├── catalog-info.yaml                    # 🎯 ARCHIVO RAÍZ (Location)
├── README.md                            # 📖 Esta documentación
├── ROADIE_SETUP.md                      # 🚀 Guía de configuración Roadie
│
├── catalog/                             # 📦 Definiciones de componentes
│   ├── catalog-info.yaml               # Portal principal
│   ├── eulen-frontend-catalog.yaml     # Frontend Angular
│   ├── eulen-api-catalog.yaml          # API Node.js
│   ├── eulen-spring-catalog.yaml       # Servicio Spring Boot
│   ├── eulen-api.yaml                  # Definición API
│   ├── eulen-system.yaml               # Sistema eulen-platform
│   ├── groups.yaml                     # Grupos y equipos
│   └── openapi.yaml                    # Especificación OpenAPI
│
└── scaffolder-templates/                # 🎨 Templates de software
    ├── README.md
    ├── angular-component.yaml
    ├── nodejs-api.yaml
    ├── spring-boot-service.yaml
    └── skeleton/
        ├── angular/
        ├── nodejs-api/
        └── spring-boot/
```

## 🔗 Registro en Roadie

### URL de Registro

```
https://github.com/AngC1/Roadie/blob/main/catalog-info.yaml
```

### Pasos

1. Ve a https://ayesa.roadie.so/
2. Catalog → Register Existing Component
3. Pega la URL anterior
4. Click "Analyze" → "Import"

### Verificación

Después de importar, deberías ver:
- ✅ 4 Componentes (portal, frontend, api, spring)
- ✅ 1 API (eulen-rest-api)
- ✅ 1 Sistema (eulen-platform)
- ✅ 4 Grupos (engineering, team-eulen, frontend, backend)
- ✅ 3 Templates (Angular, Node.js, Spring Boot)

## 🛠️ Mantenimiento

### Actualizar un Componente

1. Edita el archivo correspondiente en `catalog/`
2. Commit y push
3. Roadie refresca automáticamente (1-2 min)

### Añadir un Componente Nuevo

1. Crea archivo en `catalog/nuevo-componente.yaml`
2. Añade la ruta en `catalog-info.yaml` targets
3. Commit y push
4. Verifica en Roadie

### Eliminar un Componente

1. Elimina el archivo de `catalog/`
2. Elimina la entrada de `catalog-info.yaml` targets
3. Commit y push
4. En Roadie: Catalog → Componente → Unregister

## 📚 Recursos

- [Documentación Backstage](https://backstage.io/docs)
- [Roadie Docs](https://roadie.io/docs)
- [Backstage System Model](https://backstage.io/docs/features/software-catalog/system-model)
- [Software Templates](https://backstage.io/docs/features/software-templates/)

## 🤝 Contribución

Para contribuir al catálogo:

1. **Clona el repositorio**
2. **Usa GitHub Copilot** para generar cambios
3. **Valida** con `@workspace` antes de commit
4. **Prueba** en una rama feature primero
5. **Crea PR** con descripción clara
6. **Verifica** import en Roadie antes de merge

---

**Instancia Roadie**: https://ayesa.roadie.so/  
**Repositorio**: https://github.com/AngC1/Roadie  
**Mantenido por**: team-eulen
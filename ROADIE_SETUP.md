# Roadie Backstage Catalog - Eulen Platform

Este repositorio contiene la definición del catálogo Backstage para la plataforma Eulen en Roadie.io.

## Registro en Roadie.io

### URLs válidas para registrar

Usa **UNA** de estas URLs en Roadie → Catalog → Register Existing Component:

1. **Repositorio completo** (RECOMENDADO):
   ```
   https://github.com/AngC1/Roadie
   ```

2. **Archivo raíz directo**:
   ```
   https://github.com/AngC1/Roadie/blob/main/catalog-info.yaml
   ```

3. **Formato raw** (si las anteriores fallan):
   ```
   https://raw.githubusercontent.com/AngC1/Roadie/main/catalog-info.yaml
   ```

### ⚠️ NO usar

- ❌ `https://github.com/AngC1/Roadie/blob/main/catalog/catalog-info.yaml` (componente hijo)
- ❌ URLs con `/raw/` en posición incorrecta

## Componentes incluidos

Este catálogo define:

- **Sistema**: `eulen-platform`
- **Componentes**:
  - `eulen-portal` - Portal web principal
  - `eulen-frontend` - Aplicación Angular
  - `eulen-api` - API REST Node.js/Express
  - `eulen-spring` - Servicio backend Spring Boot
- **API**: `eulen-rest-api`
- **Grupos**:
  - `engineering` (organización)
  - `team-eulen` (equipo principal)
  - `team-eulen-frontend` (equipo frontend)
  - `team-eulen-backend` (equipo backend)

## Estructura del repositorio

```
catalog-info.yaml              # Archivo raíz (Location) - REGISTRAR ESTE
├── catalog/
│   ├── catalog-info.yaml      # Componente eulen-portal
│   ├── eulen-frontend-catalog.yaml
│   ├── eulen-api-catalog.yaml
│   ├── eulen-spring-catalog.yaml
│   ├── eulen-api.yaml         # Definición API
│   ├── eulen-system.yaml      # Sistema eulen-platform
│   ├── groups.yaml            # Grupos y equipos
│   └── openapi.yaml           # Especificación OpenAPI
```

## Pasos para registrar en Roadie

1. **Instalar GitHub App**:
   - Ve a https://ayesa.roadie.so/
   - Administration → Integrations → GitHub
   - Install GitHub App
   - Selecciona repositorio: `AngC1/Roadie`

2. **Registrar componentes**:
   - Catalog → Register Existing Component
   - Pega URL: `https://github.com/AngC1/Roadie`
   - Click "Analyze"
   - Click "Import"

3. **Verificar**:
   - Busca "eulen" en el catálogo
   - Verifica que aparecen todos los componentes
   - Revisa las relaciones de dependencia

## Troubleshooting

### Error: "Unable to read url" o "Invalid GitHub URL"

- ✅ Usa solo las URLs listadas arriba
- ✅ Verifica que la GitHub App esté instalada
- ✅ Confirma que el repo tiene acceso en Settings → Applications → GitHub Apps

### Error: "Expected Location, found Component"

- Estás usando la URL incorrecta (`/catalog/catalog-info.yaml`)
- Usa la URL raíz sin `/catalog/`

### Componentes no aparecen

- Espera 30-60 segundos (reindex automático)
- O fuerza refresh: Administration → Catalog → Refresh

### Grupos no visibles

- Los grupos pueden tardar más en indexarse
- Verifica en Settings → Organization → Teams

## Próximos pasos

- [ ] Configurar TechDocs (mkdocs.yml)
- [ ] Añadir anotaciones CI/CD (GitHub Actions)
- [ ] Integrar métricas (SonarQube, Sentry)
- [ ] Definir templates de software

## Contacto

Instancia Roadie: https://ayesa.roadie.so/
Repositorio: https://github.com/AngC1/Roadie

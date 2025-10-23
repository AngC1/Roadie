# Roadie

## Cómo Crear tu Primer Componente en Roadie.io

Este repositorio contiene ejemplos y guías para crear componentes personalizados en Roadie.io, una plataforma de portal de desarrolladores basada en Backstage.

---

## 📖 Documentación

- 📚 **[Índice de Documentación](docs/INDEX.md)** - Navegación completa de todos los recursos
- ⚡ **[Guía de Inicio Rápido](docs/GUIA-INICIO-RAPIDO.md)** - Tutorial de 10 minutos
- 🎓 **[Ejemplos Avanzados](docs/EJEMPLOS-AVANZADOS.md)** - Patrones y técnicas avanzadas
- ❓ **[FAQ](docs/FAQ.md)** - Preguntas frecuentes (Español/English)
- 🤝 **[Guía de Contribución](CONTRIBUTING.md)** - Cómo contribuir al proyecto
- 💻 **[Ejemplo de Código](examples/my-first-component/)** - Componente funcional completo

---

### ¿Qué es Roadie.io?

Roadie.io es una versión gestionada de Backstage de Spotify. Backstage es una plataforma de código abierto para construir portales de desarrolladores que unifican todas tus herramientas, servicios y documentación.

### Estructura Básica de un Componente

Un componente en Roadie.io/Backstage típicamente consiste en:

1. **Frontend Plugin** - La interfaz de usuario del componente
2. **Backend Plugin** (opcional) - La lógica del servidor
3. **catalog-info.yaml** - Archivo de configuración del componente

### Pasos para Crear tu Primer Componente

#### 1. Configurar el Entorno de Desarrollo

```bash
# Instalar Node.js (versión 18 o superior)
# Verificar instalación
node --version
npm --version

# Instalar Yarn
npm install -g yarn
```

#### 2. Crear un Nuevo Plugin de Frontend

```bash
# Crear un nuevo plugin usando el CLI de Backstage
npx @backstage/create-app

# Navegar al directorio del proyecto
cd my-roadie-app

# Crear un nuevo plugin
yarn new --select plugin

# Nombrar tu plugin (ejemplo: my-first-component)
```

#### 3. Estructura del Plugin

```
plugins/
  my-first-component/
    src/
      components/
        ExampleComponent/
          ExampleComponent.tsx
          ExampleComponent.test.tsx
      plugin.ts
      routes.ts
    package.json
    README.md
```

#### 4. Crear un Componente Básico

Crea el archivo `src/components/ExampleComponent/ExampleComponent.tsx`:

```typescript
import React from 'react';
import { Typography, Grid } from '@material-ui/core';
import {
  InfoCard,
  Header,
  Page,
  Content,
} from '@backstage/core-components';

export const ExampleComponent = () => {
  return (
    <Page themeId="tool">
      <Header title="Mi Primer Componente" subtitle="Bienvenido a Roadie.io" />
      <Content>
        <Grid container spacing={3} direction="column">
          <Grid item>
            <InfoCard title="Información">
              <Typography variant="body1">
                Este es tu primer componente personalizado en Roadie.io.
                Puedes personalizar este contenido según tus necesidades.
              </Typography>
            </InfoCard>
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
};
```

#### 5. Exportar el Plugin

Actualiza `src/plugin.ts`:

```typescript
import { createPlugin, createRoutableExtension } from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const myFirstComponentPlugin = createPlugin({
  id: 'my-first-component',
  routes: {
    root: rootRouteRef,
  },
});

export const MyFirstComponentPage = myFirstComponentPlugin.provide(
  createRoutableExtension({
    name: 'MyFirstComponentPage',
    component: () =>
      import('./components/ExampleComponent').then(m => m.ExampleComponent),
    mountPoint: rootRouteRef,
  }),
);
```

#### 6. Registrar el Plugin en la Aplicación

En `packages/app/src/App.tsx`:

```typescript
import { MyFirstComponentPage } from '@internal/plugin-my-first-component';

// Dentro del componente <FlatRoutes>
<Route path="/my-first-component" element={<MyFirstComponentPage />} />
```

#### 7. Añadir Navegación

En `packages/app/src/components/Root/Root.tsx`:

```typescript
import ExtensionIcon from '@material-ui/icons/Extension';

// Dentro del <SidebarPage>
<SidebarItem icon={ExtensionIcon} to="my-first-component" text="Mi Componente" />
```

#### 8. Ejecutar en Desarrollo

```bash
# Instalar dependencias
yarn install

# Ejecutar en modo desarrollo
yarn dev
```

Visita `http://localhost:3000/my-first-component` para ver tu componente.

### Integración con Roadie.io

Para integrar tu componente con Roadie.io:

1. **Crea un repositorio Git** para tu plugin
2. **Publica tu plugin** como paquete npm (privado o público)
3. **Configura Roadie.io** para usar tu plugin desde la UI de administración
4. **Añade el plugin** en la configuración de Roadie

### catalog-info.yaml Ejemplo

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: mi-primer-componente
  description: Mi primer componente personalizado en Roadie
  annotations:
    github.com/project-slug: tu-usuario/tu-repo
spec:
  type: library
  lifecycle: experimental
  owner: tu-equipo
```

### Recursos Adicionales

- [Documentación oficial de Backstage](https://backstage.io/docs/overview/what-is-backstage)
- [Documentación de Roadie.io](https://roadie.io/docs/)
- [Guía de desarrollo de plugins](https://backstage.io/docs/plugins/)
- [Backstage Plugin Marketplace](https://backstage.io/plugins)

### Mejores Prácticas

1. **Mantén los componentes pequeños y enfocados** - Un componente debe hacer una cosa bien
2. **Usa TypeScript** - Proporciona mejor seguridad de tipos
3. **Escribe pruebas** - Usa Jest y React Testing Library
4. **Documenta tu código** - Incluye READMEs claros y comentarios
5. **Sigue las convenciones de Backstage** - Usa los componentes base proporcionados
6. **Versiona correctamente** - Usa semántica de versionado

### Solución de Problemas

#### Error: Module not found
```bash
# Limpiar caché y reinstalar
yarn clean
yarn install
```

#### Puerto en uso
```bash
# Cambiar el puerto en package.json o usar:
PORT=3001 yarn dev
```

#### Problemas de compilación TypeScript
```bash
# Verificar versiones
yarn tsc --version

# Limpiar y reconstruir
yarn clean
yarn build
```

---

## How to Create Your First Component in Roadie.io

This repository contains examples and guides for creating custom components in Roadie.io, a developer portal platform based on Backstage.

### What is Roadie.io?

Roadie.io is a managed version of Spotify's Backstage. Backstage is an open-source platform for building developer portals that unify all your tools, services, and documentation.

### Basic Component Structure

A component in Roadie.io/Backstage typically consists of:

1. **Frontend Plugin** - The user interface component
2. **Backend Plugin** (optional) - Server-side logic
3. **catalog-info.yaml** - Component configuration file

### Steps to Create Your First Component

#### 1. Setup Development Environment

```bash
# Install Node.js (version 18 or higher)
# Verify installation
node --version
npm --version

# Install Yarn
npm install -g yarn
```

#### 2. Create a New Frontend Plugin

```bash
# Create a new plugin using Backstage CLI
npx @backstage/create-app

# Navigate to project directory
cd my-roadie-app

# Create a new plugin
yarn new --select plugin

# Name your plugin (example: my-first-component)
```

#### 3. Plugin Structure

```
plugins/
  my-first-component/
    src/
      components/
        ExampleComponent/
          ExampleComponent.tsx
          ExampleComponent.test.tsx
      plugin.ts
      routes.ts
    package.json
    README.md
```

#### 4. Create a Basic Component

Create file `src/components/ExampleComponent/ExampleComponent.tsx`:

```typescript
import React from 'react';
import { Typography, Grid } from '@material-ui/core';
import {
  InfoCard,
  Header,
  Page,
  Content,
} from '@backstage/core-components';

export const ExampleComponent = () => {
  return (
    <Page themeId="tool">
      <Header title="My First Component" subtitle="Welcome to Roadie.io" />
      <Content>
        <Grid container spacing={3} direction="column">
          <Grid item>
            <InfoCard title="Information">
              <Typography variant="body1">
                This is your first custom component in Roadie.io.
                You can customize this content according to your needs.
              </Typography>
            </InfoCard>
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
};
```

#### 5. Export the Plugin

Update `src/plugin.ts`:

```typescript
import { createPlugin, createRoutableExtension } from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const myFirstComponentPlugin = createPlugin({
  id: 'my-first-component',
  routes: {
    root: rootRouteRef,
  },
});

export const MyFirstComponentPage = myFirstComponentPlugin.provide(
  createRoutableExtension({
    name: 'MyFirstComponentPage',
    component: () =>
      import('./components/ExampleComponent').then(m => m.ExampleComponent),
    mountPoint: rootRouteRef,
  }),
);
```

#### 6. Register Plugin in Application

In `packages/app/src/App.tsx`:

```typescript
import { MyFirstComponentPage } from '@internal/plugin-my-first-component';

// Inside <FlatRoutes> component
<Route path="/my-first-component" element={<MyFirstComponentPage />} />
```

#### 7. Add Navigation

In `packages/app/src/components/Root/Root.tsx`:

```typescript
import ExtensionIcon from '@material-ui/icons/Extension';

// Inside <SidebarPage>
<SidebarItem icon={ExtensionIcon} to="my-first-component" text="My Component" />
```

#### 8. Run in Development

```bash
# Install dependencies
yarn install

# Run in development mode
yarn dev
```

Visit `http://localhost:3000/my-first-component` to see your component.

### Integration with Roadie.io

To integrate your component with Roadie.io:

1. **Create a Git repository** for your plugin
2. **Publish your plugin** as npm package (private or public)
3. **Configure Roadie.io** to use your plugin from admin UI
4. **Add the plugin** in Roadie configuration

### Example catalog-info.yaml

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-first-component
  description: My first custom component in Roadie
  annotations:
    github.com/project-slug: your-user/your-repo
spec:
  type: library
  lifecycle: experimental
  owner: your-team
```

### Additional Resources

- [Official Backstage Documentation](https://backstage.io/docs/overview/what-is-backstage)
- [Roadie.io Documentation](https://roadie.io/docs/)
- [Plugin Development Guide](https://backstage.io/docs/plugins/)
- [Backstage Plugin Marketplace](https://backstage.io/plugins)

### Best Practices

1. **Keep components small and focused** - A component should do one thing well
2. **Use TypeScript** - Provides better type safety
3. **Write tests** - Use Jest and React Testing Library
4. **Document your code** - Include clear READMEs and comments
5. **Follow Backstage conventions** - Use provided base components
6. **Version properly** - Use semantic versioning

### Troubleshooting

#### Error: Module not found
```bash
# Clear cache and reinstall
yarn clean
yarn install
```

#### Port in use
```bash
# Change port in package.json or use:
PORT=3001 yarn dev
```

#### TypeScript compilation issues
```bash
# Check versions
yarn tsc --version

# Clean and rebuild
yarn clean
yarn build
```
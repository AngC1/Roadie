# Guía de Inicio Rápido - Roadie.io

## 🚀 Creando tu Primer Componente en 10 Minutos

Esta guía te llevará desde cero hasta tener tu primer componente funcionando en Roadie.io.

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- ✅ Node.js 18 o superior
- ✅ Yarn (gestor de paquetes)
- ✅ Git
- ✅ Editor de código (recomendado: VS Code)

### Paso 1: Verificar Instalación (2 minutos)

```bash
# Verificar Node.js
node --version
# Debería mostrar: v18.x.x o superior

# Verificar Yarn
yarn --version
# Debería mostrar: 1.22.x o superior

# Si no tienes Yarn instalado:
npm install -g yarn
```

### Paso 2: Crear Aplicación Backstage (3 minutos)

```bash
# Crear una nueva aplicación Backstage
npx @backstage/create-app@latest

# Cuando te pregunte el nombre, escribe:
# my-roadie-app

# Navegar al directorio
cd my-roadie-app
```

**¿Qué acabas de crear?**
- Una aplicación completa de Backstage
- Frontend y Backend configurados
- Ejemplo de plugins incluidos
- Base de datos SQLite para desarrollo

### Paso 3: Crear tu Primer Plugin (2 minutos)

```bash
# Desde el directorio my-roadie-app
yarn new --select plugin

# Cuando te pregunte:
# - Plugin ID: my-first-component
# - Owner: [tu nombre o equipo]
```

**¿Qué acabas de crear?**
- Un nuevo plugin en `plugins/my-first-component`
- Estructura completa de archivos
- Configuración de dependencias
- Plantilla básica del componente

### Paso 4: Personalizar el Componente (2 minutos)

Abre el archivo `plugins/my-first-component/src/components/ExampleComponent/ExampleComponent.tsx` y reemplaza su contenido con:

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
      <Header 
        title="¡Hola Roadie.io!" 
        subtitle="Mi primer componente personalizado 🎉"
      />
      <Content>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <InfoCard title="¡Felicidades!">
              <Typography variant="body1">
                Has creado exitosamente tu primer componente en Roadie.io.
                Este es el comienzo de tu viaje en el desarrollo de portales
                para desarrolladores.
              </Typography>
            </InfoCard>
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
};
```

### Paso 5: Ejecutar en Desarrollo (1 minuto)

```bash
# Instalar dependencias (primera vez solamente)
yarn install

# Iniciar servidor de desarrollo
yarn dev
```

**Espera a que veas:**
```
[0] webpack compiled successfully
[1] Backend started on port 7007
```

### Paso 6: Ver tu Componente

1. Abre tu navegador en: `http://localhost:3000`
2. Navega a: `http://localhost:3000/my-first-component`
3. ¡Verás tu componente funcionando! 🎊

## 🎯 Próximos Pasos

### Agregar Navegación

Para que tu componente aparezca en el menú lateral:

1. Abre `packages/app/src/components/Root/Root.tsx`
2. Agrega al final de los imports:
```typescript
import ExtensionIcon from '@material-ui/icons/Extension';
```
3. Dentro de `<SidebarPage>`, agrega:
```typescript
<SidebarItem 
  icon={ExtensionIcon} 
  to="my-first-component" 
  text="Mi Componente" 
/>
```

### Personalizar el Diseño

Prueba cambiar el `themeId` en tu componente:

- `tool` - Tema verde (herramientas)
- `website` - Tema azul (sitios web)
- `service` - Tema naranja (servicios)
- `documentation` - Tema morado (documentación)
- `library` - Tema rosa (bibliotecas)

```typescript
<Page themeId="website"> {/* Cambia a tu tema preferido */}
```

### Agregar Más Contenido

Agrega más tarjetas de información:

```typescript
<Grid item xs={12} md={6}>
  <InfoCard title="Característica 1">
    <Typography>Descripción de la característica</Typography>
  </InfoCard>
</Grid>
<Grid item xs={12} md={6}>
  <InfoCard title="Característica 2">
    <Typography>Otra descripción</Typography>
  </InfoCard>
</Grid>
```

## 🐛 Solución de Problemas Comunes

### El puerto 3000 está en uso

```bash
# Usa un puerto diferente
PORT=3001 yarn dev
```

### Error de módulo no encontrado

```bash
# Limpia y reinstala
yarn clean
yarn install
```

### Cambios no se reflejan

1. Detén el servidor (Ctrl+C)
2. Limpia la caché:
```bash
yarn clean
```
3. Reinicia:
```bash
yarn dev
```

## 📚 Recursos de Aprendizaje

### Documentación Oficial
- [Backstage Docs](https://backstage.io/docs/)
- [Roadie.io Docs](https://roadie.io/docs/)

### Tutoriales
- [Plugin Development](https://backstage.io/docs/plugins/)
- [Material-UI Components](https://v4.mui.com/)

### Comunidad
- [Discord de Backstage](https://discord.gg/backstage)
- [GitHub Discussions](https://github.com/backstage/backstage/discussions)

## ✅ Checklist de Completación

¿Completaste todos los pasos? Marca los que hayas hecho:

- [ ] Instalé Node.js y Yarn
- [ ] Creé mi aplicación Backstage
- [ ] Generé mi primer plugin
- [ ] Personalicé el componente
- [ ] Lo ejecuté en desarrollo
- [ ] Vi mi componente en el navegador
- [ ] Agregué navegación en el menú
- [ ] Personalicé el diseño

## 🎓 Siguiente Nivel

Una vez que completes esta guía, estás listo para:

1. **Conectar con APIs** - Obtener datos de servicios externos
2. **Agregar Backend** - Crear lógica del servidor
3. **Integrar con el Catálogo** - Mostrar componentes registrados
4. **Crear Visualizaciones** - Gráficos y dashboards
5. **Publicar tu Plugin** - Compartir con otros equipos

¡Feliz desarrollo! 🚀

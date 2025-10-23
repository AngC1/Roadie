# Mi Primer Componente - Roadie.io Plugin

Este es un ejemplo de plugin básico para Roadie.io/Backstage que muestra cómo crear tu primer componente personalizado.

## Características

- ✨ Componente React simple y funcional
- 🎨 Utiliza Material-UI para el diseño
- 📦 Integrado con la arquitectura de plugins de Backstage
- 🧪 Incluye pruebas unitarias
- 📝 Documentación completa

## Instalación

```bash
# Instalar dependencias
yarn install

# Ejecutar en modo desarrollo
yarn start

# Ejecutar pruebas
yarn test

# Construir para producción
yarn build
```

## Estructura del Proyecto

```
my-first-component/
├── src/
│   ├── components/
│   │   └── ExampleComponent/
│   │       ├── ExampleComponent.tsx      # Componente principal
│   │       ├── ExampleComponent.test.tsx # Pruebas unitarias
│   │       └── index.ts                  # Exportaciones
│   ├── plugin.ts                         # Definición del plugin
│   ├── routes.ts                         # Rutas del plugin
│   └── index.ts                          # Punto de entrada
├── package.json
└── README.md
```

## Uso

### En una aplicación Backstage

1. Instala el plugin:
```bash
yarn workspace app add @internal/plugin-my-first-component
```

2. Importa y usa el componente en `packages/app/src/App.tsx`:
```typescript
import { MyFirstComponentPage } from '@internal/plugin-my-first-component';

// Dentro de <FlatRoutes>
<Route path="/my-first-component" element={<MyFirstComponentPage />} />
```

3. Agrega navegación en `packages/app/src/components/Root/Root.tsx`:
```typescript
import ExtensionIcon from '@material-ui/icons/Extension';

<SidebarItem 
  icon={ExtensionIcon} 
  to="my-first-component" 
  text="Mi Componente" 
/>
```

## Personalización

### Cambiar el tema

Modifica el `themeId` en `ExampleComponent.tsx`:
```typescript
<Page themeId="tool"> {/* opciones: tool, website, service, documentation, etc. */}
```

### Agregar más funcionalidades

Puedes extender el componente agregando:
- Llamadas a APIs externas
- Estado local con hooks de React
- Integración con el catálogo de Backstage
- Conexión con otros plugins

## Próximos Pasos

1. **Personaliza el diseño** - Modifica los estilos y el contenido
2. **Agrega funcionalidad** - Conecta con APIs o servicios
3. **Escribe más pruebas** - Asegura la calidad del código
4. **Documenta tu plugin** - Ayuda a otros a usar tu componente
5. **Publica tu plugin** - Comparte con la comunidad

## Recursos

- [Documentación de Backstage](https://backstage.io/docs/)
- [Documentación de Roadie.io](https://roadie.io/docs/)
- [Material-UI](https://v4.mui.com/)
- [React](https://reactjs.org/)

## Licencia

MIT

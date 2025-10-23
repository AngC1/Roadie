# Preguntas Frecuentes (FAQ) / Frequently Asked Questions

## 🇪🇸 Español

### ¿Qué es Roadie.io?

Roadie.io es una versión gestionada en la nube de Backstage, la plataforma de portal de desarrolladores de código abierto creada por Spotify. Elimina la complejidad de hospedar y mantener Backstage, permitiéndote enfocarte en crear valor para tus equipos.

### ¿Por qué debería crear un componente personalizado?

Los componentes personalizados te permiten:
- Integrar herramientas y servicios específicos de tu organización
- Mostrar datos personalizados relevantes para tus equipos
- Crear flujos de trabajo específicos
- Mejorar la experiencia de desarrollador con funcionalidades únicas

### ¿Necesito conocimientos de React?

Sí, es recomendable tener conocimientos básicos de:
- React (hooks, componentes funcionales)
- TypeScript
- Material-UI
- Conceptos básicos de APIs

### ¿Cuánto tiempo toma crear un componente básico?

Para un desarrollador con experiencia en React:
- Componente simple: 1-2 horas
- Componente con integración API: 3-5 horas
- Componente complejo con backend: 1-2 días

### ¿Puedo usar librerías externas?

Sí, puedes instalar y usar cualquier librería de npm compatible con React. Algunas recomendadas:
- `chart.js` / `recharts` - Para gráficos
- `react-query` - Para manejo de datos
- `date-fns` - Para manejo de fechas
- `lodash` - Utilidades

### ¿Cómo pruebo mi componente localmente?

```bash
# En el directorio de tu aplicación Backstage
yarn dev
```

Esto iniciará un servidor de desarrollo en `http://localhost:3000`

### ¿Cómo despliego mi componente a Roadie.io?

1. Publica tu plugin como paquete npm
2. Accede a Roadie.io Admin
3. Navega a "Settings" > "Plugins"
4. Agrega tu plugin desde npm
5. Configura y habilita el plugin

### ¿Puedo compartir mi componente con otros?

Sí! Puedes:
- Publicarlo en npm como paquete público
- Compartirlo en el [Backstage Plugin Marketplace](https://backstage.io/plugins)
- Contribuirlo como código abierto

### ¿Qué sucede si encuentro un error?

1. Verifica los logs en la consola del navegador
2. Revisa los logs del backend (si aplica)
3. Consulta la [documentación de Backstage](https://backstage.io/docs/)
4. Pregunta en el [Discord de Backstage](https://discord.gg/backstage)
5. Busca en [GitHub Discussions](https://github.com/backstage/backstage/discussions)

### ¿Cómo actualizo mi componente?

1. Haz cambios en tu código
2. Incrementa la versión en `package.json`
3. Publica la nueva versión en npm
4. Actualiza el plugin en Roadie.io Admin

---

## 🇬🇧 English

### What is Roadie.io?

Roadie.io is a managed cloud version of Backstage, the open-source developer portal platform created by Spotify. It removes the complexity of hosting and maintaining Backstage, allowing you to focus on creating value for your teams.

### Why should I create a custom component?

Custom components allow you to:
- Integrate tools and services specific to your organization
- Display custom data relevant to your teams
- Create specific workflows
- Improve developer experience with unique features

### Do I need React knowledge?

Yes, it's recommended to have basic knowledge of:
- React (hooks, functional components)
- TypeScript
- Material-UI
- Basic API concepts

### How long does it take to create a basic component?

For a developer with React experience:
- Simple component: 1-2 hours
- Component with API integration: 3-5 hours
- Complex component with backend: 1-2 days

### Can I use external libraries?

Yes, you can install and use any React-compatible npm library. Some recommended:
- `chart.js` / `recharts` - For charts
- `react-query` - For data management
- `date-fns` - For date handling
- `lodash` - Utilities

### How do I test my component locally?

```bash
# In your Backstage application directory
yarn dev
```

This will start a development server at `http://localhost:3000`

### How do I deploy my component to Roadie.io?

1. Publish your plugin as an npm package
2. Access Roadie.io Admin
3. Navigate to "Settings" > "Plugins"
4. Add your plugin from npm
5. Configure and enable the plugin

### Can I share my component with others?

Yes! You can:
- Publish it on npm as a public package
- Share it on the [Backstage Plugin Marketplace](https://backstage.io/plugins)
- Contribute it as open source

### What if I encounter an error?

1. Check the browser console logs
2. Review backend logs (if applicable)
3. Consult [Backstage documentation](https://backstage.io/docs/)
4. Ask on [Backstage Discord](https://discord.gg/backstage)
5. Search in [GitHub Discussions](https://github.com/backstage/backstage/discussions)

### How do I update my component?

1. Make changes to your code
2. Increment the version in `package.json`
3. Publish the new version to npm
4. Update the plugin in Roadie.io Admin

---

## 🔧 Problemas Comunes / Common Issues

### Error: "Module not found"

**Español:** Ejecuta `yarn clean && yarn install` para limpiar la caché y reinstalar dependencias.

**English:** Run `yarn clean && yarn install` to clear cache and reinstall dependencies.

### Error: "Port 3000 is already in use"

**Español:** Usa un puerto diferente: `PORT=3001 yarn dev`

**English:** Use a different port: `PORT=3001 yarn dev`

### Los cambios no se reflejan / Changes not reflecting

**Español:**
1. Detén el servidor (Ctrl+C)
2. Ejecuta `yarn clean`
3. Inicia nuevamente: `yarn dev`

**English:**
1. Stop the server (Ctrl+C)
2. Run `yarn clean`
3. Start again: `yarn dev`

### Error de TypeScript / TypeScript Error

**Español:** Asegúrate de que todas las dependencias de tipos estén instaladas:
```bash
yarn add -D @types/react @types/node
```

**English:** Ensure all type dependencies are installed:
```bash
yarn add -D @types/react @types/node
```

---

## 📚 Recursos Adicionales / Additional Resources

### Documentación / Documentation
- [Backstage Official Docs](https://backstage.io/docs/)
- [Roadie.io Docs](https://roadie.io/docs/)
- [Material-UI v4](https://v4.mui.com/)
- [React Documentation](https://reactjs.org/)

### Comunidad / Community
- [Backstage Discord](https://discord.gg/backstage)
- [GitHub Discussions](https://github.com/backstage/backstage/discussions)
- [Roadie Blog](https://roadie.io/blog/)

### Tutoriales / Tutorials
- [Backstage Plugin Development](https://backstage.io/docs/plugins/)
- [Creating Custom Plugins](https://backstage.io/docs/plugins/create-a-plugin)
- [Roadie Getting Started](https://roadie.io/docs/getting-started/)

---

¿Tienes más preguntas? / Have more questions?

Abre un issue en este repositorio o contacta con la comunidad de Backstage.

Open an issue in this repository or contact the Backstage community.

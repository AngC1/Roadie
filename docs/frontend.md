# Eulen Frontend

Aplicación Angular moderna para la Plataforma Eulen.

## 🎯 Descripción

El frontend de Eulen es una aplicación de página única (SPA) construida con Angular 17+, que proporciona una interfaz de usuario intuitiva y moderna.

## 🛠️ Tecnologías

- **Framework**: Angular 17+
- **Lenguaje**: TypeScript 5.2+
- **Estilos**: SCSS/CSS
- **State Management**: NgRx (opcional)
- **UI Components**: Angular Material

## 📦 Instalación

### Prerrequisitos

```bash
node --version  # v18.0.0 o superior
npm --version   # v9.0.0 o superior
```

### Pasos de Instalación

```bash
# Clonar repositorio
git clone https://github.com/AngC1/Roadie.git
cd Roadie/src/app

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

La aplicación estará disponible en `http://localhost:4200/`

## 🏗️ Estructura del Proyecto

```
src/
├── app/
│   ├── components/        # Componentes reutilizables
│   ├── pages/            # Páginas/vistas principales
│   ├── services/         # Servicios Angular
│   ├── models/           # Interfaces y modelos TypeScript
│   ├── guards/           # Route guards
│   └── interceptors/     # HTTP interceptors
├── assets/               # Recursos estáticos
├── environments/         # Configuraciones por ambiente
└── styles/              # Estilos globales
```

## 🔧 Configuración

### Variables de Entorno

Edita `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api/v1',
  apiTimeout: 30000
};
```

### Proxy de Desarrollo

Configura `proxy.conf.json` para desarrollo local:

```json
{
  "/api": {
    "target": "http://localhost:3000",
    "secure": false,
    "changeOrigin": true
  }
}
```

## 🧪 Testing

### Tests Unitarios

```bash
npm test
```

### Tests E2E

```bash
npm run e2e
```

### Cobertura

```bash
npm run test:coverage
```

## 🚀 Compilación

### Build de Desarrollo

```bash
npm run build
```

### Build de Producción

```bash
npm run build:prod
```

Los archivos compilados estarán en `dist/`

## 📐 Convenciones de Código

### Nomenclatura

- **Componentes**: PascalCase (`UserProfileComponent`)
- **Servicios**: PascalCase + Service (`AuthService`)
- **Variables**: camelCase (`userName`)
- **Constantes**: UPPER_SNAKE_CASE (`API_URL`)

### Organización de Archivos

- Un componente por archivo
- Nombre de archivo: `kebab-case.component.ts`
- Test junto al componente: `component-name.component.spec.ts`

## 🔌 Integración con API

### Consumo de API REST

```typescript
import { HttpClient } from '@angular/common/http';

@Injectable()
export class DataService {
  constructor(private http: HttpClient) {}
  
  getData() {
    return this.http.get('/api/v1/data');
  }
}
```

### Manejo de Errores

```typescript
import { catchError } from 'rxjs/operators';

getData() {
  return this.http.get('/api/v1/data').pipe(
    catchError(this.handleError)
  );
}
```

## 🎨 Guía de Estilos

- Utiliza Angular Material para componentes UI
- Sigue las guías de estilo de Angular oficial
- Mantén componentes pequeños y enfocados
- Usa servicios para lógica de negocio

## 🔐 Autenticación

El frontend implementa autenticación mediante:
- Guards para protección de rutas
- Interceptores HTTP para tokens
- Manejo de sesión local

## 📱 Responsive Design

La aplicación está optimizada para:
- Desktop (1920px+)
- Tablet (768px - 1919px)
- Mobile (< 768px)

## 🐛 Debugging

### Modo Debug

```bash
ng serve --configuration=debug
```

### DevTools

- Angular DevTools (extensión de Chrome)
- Redux DevTools (si usas NgRx)

## 📚 Recursos Adicionales

- [Angular Documentation](https://angular.io/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Angular Material](https://material.angular.io/)

## 👥 Equipo

**Owner**: team-eulen-frontend

## 🔗 Enlaces

- [API Documentation](./api.md)
- [Architecture Overview](./index.md)

# Eulen API

API REST construida con Node.js y Express para la Plataforma Eulen.

## 🎯 Descripción

La API de Eulen proporciona servicios REST para todas las operaciones de la plataforma, incluyendo gestión de datos, autenticación y lógica de negocio.

## 🛠️ Tecnologías

- **Runtime**: Node.js 18+
- **Framework**: Express.js 4.18+
- **Lenguaje**: JavaScript (ES6+)
- **Base de Datos**: PostgreSQL / MongoDB
- **Autenticación**: JWT
- **Validación**: Joi / Express-validator

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
cd Roadie/src/api

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Iniciar servidor de desarrollo
npm run dev
```

La API estará disponible en `http://localhost:3000/`

## 🏗️ Estructura del Proyecto

```
src/
├── api/
│   ├── controllers/      # Controladores de rutas
│   ├── services/         # Lógica de negocio
│   ├── models/           # Modelos de datos
│   ├── middleware/       # Middlewares Express
│   ├── routes/           # Definición de rutas
│   ├── validators/       # Validadores de entrada
│   └── utils/            # Utilidades y helpers
├── config/               # Configuraciones
└── tests/               # Tests automatizados
```

## 🔧 Configuración

### Variables de Entorno

Crea archivo `.env`:

```bash
# Server
PORT=3000
NODE_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eulen_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your_jwt_secret
JWT_EXPIRATION=24h

# CORS
CORS_ORIGIN=http://localhost:4200
```

## 📡 Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "OK",
  "service": "eulen-api",
  "timestamp": "2025-10-26T10:00:00.000Z"
}
```

### Authentication

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Data Operations

```http
GET /api/v1/data
Authorization: Bearer {token}
```

**Response:**
```json
{
  "data": [...],
  "total": 100,
  "page": 1,
  "pageSize": 20
}
```

## 🧪 Testing

### Tests Unitarios

```bash
npm test
```

### Tests de Integración

```bash
npm run test:integration
```

### Cobertura

```bash
npm run test:coverage
```

## 🔐 Seguridad

### Implementaciones

- **Helmet**: Headers de seguridad HTTP
- **CORS**: Control de acceso cross-origin
- **Rate Limiting**: Límite de peticiones
- **Input Validation**: Validación de todas las entradas
- **SQL Injection Protection**: Queries parametrizadas
- **XSS Protection**: Sanitización de datos

### Ejemplo de Middleware de Seguridad

```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

app.use(helmet());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));
```

## 📊 Logging

### Configuración

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Uso

```javascript
logger.info('User logged in', { userId: user.id });
logger.error('Database connection failed', { error });
```

## 🚀 Despliegue

### Build de Producción

```bash
npm run build
npm start
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Construcción de Imagen

```bash
docker build -t eulen-api .
docker run -p 3000:3000 eulen-api
```

## 📐 Convenciones de Código

### Estructura de Controladores

```javascript
// controllers/userController.js
exports.getUser = async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    res.json({ data: user });
  } catch (error) {
    next(error);
  }
};
```

### Manejo de Errores

```javascript
// middleware/errorHandler.js
module.exports = (err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  
  logger.error(message, { error: err, url: req.url });
  
  res.status(status).json({
    error: {
      message,
      status
    }
  });
};
```

## 🔌 Integración con Servicios

### Base de Datos

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
});
```

### Redis Cache

```javascript
const redis = require('redis');
const client = redis.createClient({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});
```

## 📈 Monitoreo

### Métricas con Prometheus

```javascript
const promClient = require('prom-client');
const register = new promClient.Registry();

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
});

register.registerMetric(httpRequestDuration);
```

## 📚 Documentación API

La documentación OpenAPI completa está disponible en:
- Desarrollo: http://localhost:3000/api-docs
- Producción: https://api.eulen.ayesa.com/api-docs

Archivo: `catalog/openapi.yaml`

## 🐛 Debugging

### Modo Debug

```bash
DEBUG=* npm run dev
```

### VS Code Launch Config

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug API",
  "program": "${workspaceFolder}/src/index.js",
  "env": {
    "NODE_ENV": "development"
  }
}
```

## 👥 Equipo

**Owner**: team-eulen-backend

## 🔗 Enlaces

- [Frontend Documentation](./frontend.md)
- [Spring Service Documentation](./spring.md)
- [OpenAPI Specification](https://github.com/AngC1/Roadie/blob/main/catalog/openapi.yaml)

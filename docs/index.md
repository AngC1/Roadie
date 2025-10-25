# Eulen Platform

Bienvenido a la documentación de la Plataforma Eulen.

## 🏗️ Arquitectura

La Plataforma Eulen es un sistema modular compuesto por múltiples componentes que trabajan en conjunto para proporcionar una solución empresarial completa.

### Componentes Principales

#### Frontend
- **Eulen Portal**: Portal web principal de acceso
- **Eulen Frontend**: Aplicación Angular moderna con interfaz de usuario avanzada

#### Backend
- **Eulen API**: API REST basada en Node.js/Express que proporciona servicios core
- **Eulen Spring**: Microservicio Spring Boot para lógica de negocio

### Diagrama de Arquitectura

```
┌─────────────────┐
│  Eulen Portal   │
└────────┬────────┘
         │
┌────────▼────────┐       ┌──────────────────┐
│ Eulen Frontend  │◄──────┤   Eulen API      │
└─────────────────┘       └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │  Eulen Spring    │
                          └──────────────────┘
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Node.js 18+
- Java 17+
- Angular CLI 17+
- Maven 3.8+

### Instalación

Cada componente tiene sus propias instrucciones de instalación. Consulta la documentación específica de cada componente.

## 📦 Componentes

- [Frontend Angular](./frontend.md) - Aplicación de interfaz de usuario
- [API Node.js](./api.md) - Servicios REST
- [Spring Boot](./spring.md) - Microservicios empresariales

## 🔐 Seguridad

La plataforma implementa:
- Autenticación OAuth 2.0
- Autorización basada en roles
- Encriptación de datos en tránsito (HTTPS/TLS)
- Validación de entrada en todas las capas

## 🌐 Despliegue

### Ambientes

- **Desarrollo**: Para desarrollo local
- **Staging**: Para pruebas pre-producción
- **Producción**: Ambiente productivo

### CI/CD

Utilizamos GitHub Actions para:
- Compilación automática
- Ejecución de tests
- Análisis de código
- Despliegue automatizado

## 📊 Monitoreo

- **Logs**: Centralizados en ELK Stack
- **Métricas**: Prometheus + Grafana
- **Alertas**: Configuradas en Alertmanager
- **APM**: Application Performance Monitoring activo

## 🤝 Contribución

Para contribuir a la plataforma:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'feat: añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

- **Email**: team-eulen@ayesa.com
- **Roadie**: https://ayesa.roadie.so/
- **GitHub**: https://github.com/AngC1/Roadie

## 📝 Licencia

Propiedad de Ayesa © 2025

# ${{ values.name }}

${{ values.description }}

## Overview

This is a Node.js/Express API scaffolded from Roadie Backstage.

## Prerequisites

- Node.js 18+
- npm 9+

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The API will start on port ${{ values.port }}.

### Production

```bash
npm start
```

### Testing

```bash
npm test
```

## Endpoints

- Health: `GET /health`
- API Info: `GET /api/v1/`

## API Documentation

OpenAPI specification is available in `openapi.yaml`.

## Owner

This API is owned by **${{ values.owner }}**.

## System

Part of the **eulen-platform** system.

## Technology Stack

- Node.js
- Express.js
- CORS, Helmet (security)

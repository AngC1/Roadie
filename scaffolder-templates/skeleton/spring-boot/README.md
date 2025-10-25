# ${{ values.name }}

${{ values.description }}

## Overview

This is a Spring Boot microservice scaffolded from Roadie Backstage.

## Prerequisites

- Java ${{ values.javaVersion }}
- Maven 3.8+

## Getting Started

### Build

```bash
mvn clean install
```

### Run

```bash
mvn spring-boot:run
```

The service will start on port 8080.

### Test

```bash
mvn test
```

## Endpoints

- Health: `GET /actuator/health`
- Info: `GET /actuator/info`

## Owner

This service is owned by **${{ values.owner }}**.

## System

Part of the **eulen-platform** system.

## Technology Stack

- Java ${{ values.javaVersion }}
- Spring Boot ${{ values.springBootVersion }}
- Maven

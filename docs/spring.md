# Eulen Spring Service

Microservicio Spring Boot para lógica de negocio empresarial de la Plataforma Eulen.

## 🎯 Descripción

El servicio Spring Boot de Eulen implementa la lógica de negocio crítica, procesamiento de datos y servicios empresariales utilizando el ecosistema Spring.

## 🛠️ Tecnologías

- **Framework**: Spring Boot 3.2+
- **Lenguaje**: Java 17+
- **Build**: Maven 3.8+
- **Base de Datos**: JPA/Hibernate
- **Seguridad**: Spring Security
- **Messaging**: Spring Cloud Stream (opcional)

## 📦 Instalación

### Prerrequisitos

```bash
java -version   # Java 17 o superior
mvn -version    # Maven 3.8 o superior
```

### Pasos de Instalación

```bash
# Clonar repositorio
git clone https://github.com/AngC1/Roadie.git
cd Roadie/src/eulen

# Compilar
mvn clean install

# Ejecutar
mvn spring-boot:run
```

El servicio estará disponible en `http://localhost:8080/`

## 🏗️ Estructura del Proyecto

```
src/
├── main/
│   ├── java/com/ayesa/eulen/
│   │   ├── controller/       # REST Controllers
│   │   ├── service/          # Service Layer
│   │   ├── repository/       # Data Access Layer
│   │   ├── model/            # Domain Models/Entities
│   │   ├── dto/              # Data Transfer Objects
│   │   ├── config/           # Configuraciones Spring
│   │   ├── exception/        # Exception Handlers
│   │   └── util/             # Utilidades
│   └── resources/
│       ├── application.yml   # Configuración principal
│       ├── application-dev.yml
│       └── application-prod.yml
└── test/                     # Tests
```

## 🔧 Configuración

### application.yml

```yaml
server:
  port: 8080
  
spring:
  application:
    name: eulen-spring-service
    
  datasource:
    url: jdbc:postgresql://localhost:5432/eulen_db
    username: postgres
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver
    
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
        
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: ${JWT_ISSUER_URI}
          
logging:
  level:
    com.ayesa.eulen: DEBUG
    org.springframework: INFO
    
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
```

### Variables de Entorno

```bash
export DB_PASSWORD=your_password
export JWT_ISSUER_URI=https://auth.eulen.ayesa.com
```

## 📡 Endpoints

### Actuator Health

```http
GET /actuator/health
```

**Response:**
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL",
        "validationQuery": "isValid()"
      }
    }
  }
}
```

### Business Operations

```http
GET /api/v1/business/operations
Authorization: Bearer {token}
```

**Response:**
```json
{
  "operations": [...],
  "timestamp": "2025-10-26T10:00:00.000Z"
}
```

## 🏛️ Arquitectura

### Layered Architecture

```
┌─────────────────────────────┐
│      Controller Layer       │
│  (REST API Endpoints)       │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│      Service Layer          │
│  (Business Logic)           │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│    Repository Layer         │
│  (Data Access)              │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│       Database              │
└─────────────────────────────┘
```

### Ejemplo de Implementación

#### Entity

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Column(nullable = false)
    private String name;
    
    @CreatedDate
    private LocalDateTime createdAt;
    
    // Getters and Setters
}
```

#### Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);
}
```

#### Service

```java
@Service
@Transactional
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(UserDTO userDTO) {
        User user = new User();
        user.setEmail(userDTO.getEmail());
        user.setName(userDTO.getName());
        return userRepository.save(user);
    }
    
    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }
}
```

#### Controller

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserDTO userDTO) {
        User user = userService.createUser(userDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
    
    @GetMapping("/{email}")
    public ResponseEntity<User> getUser(@PathVariable String email) {
        return userService.getUserByEmail(email)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
```

## 🧪 Testing

### Tests Unitarios

```java
@SpringBootTest
class UserServiceTest {
    
    @Autowired
    private UserService userService;
    
    @MockBean
    private UserRepository userRepository;
    
    @Test
    void shouldCreateUser() {
        UserDTO dto = new UserDTO("test@test.com", "Test User");
        when(userRepository.save(any())).thenReturn(new User());
        
        User user = userService.createUser(dto);
        
        assertNotNull(user);
        verify(userRepository).save(any());
    }
}
```

### Tests de Integración

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class UserControllerIntegrationTest {
    
    @LocalServerPort
    private int port;
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void shouldGetUser() {
        ResponseEntity<User> response = restTemplate
            .getForEntity("http://localhost:" + port + "/api/v1/users/test@test.com", User.class);
            
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }
}
```

### Ejecutar Tests

```bash
# Todos los tests
mvn test

# Solo tests unitarios
mvn test -Dtest=*Test

# Solo tests de integración
mvn test -Dtest=*IntegrationTest

# Con cobertura
mvn test jacoco:report
```

## 🔐 Seguridad

### Spring Security Configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/**").permitAll()
                .requestMatchers("/api/v1/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(OAuth2ResourceServerConfigurer::jwt);
        return http.build();
    }
}
```

### JWT Validation

```java
@Bean
public JwtDecoder jwtDecoder() {
    return JwtDecoders.fromIssuerLocation(issuerUri);
}
```

## 📊 Monitoring & Observability

### Actuator Endpoints

- `/actuator/health` - Health check
- `/actuator/info` - Application info
- `/actuator/metrics` - Métricas
- `/actuator/prometheus` - Métricas formato Prometheus

### Logging

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class BusinessService {
    
    private static final Logger log = LoggerFactory.getLogger(BusinessService.class);
    
    public void processOperation() {
        log.info("Processing operation started");
        try {
            // Business logic
            log.debug("Operation details: {}", details);
        } catch (Exception e) {
            log.error("Operation failed", e);
            throw e;
        }
    }
}
```

## 🚀 Despliegue

### Build JAR

```bash
mvn clean package -DskipTests
```

El JAR estará en `target/eulen-spring-0.1.0.jar`

### Ejecutar JAR

```bash
java -jar target/eulen-spring-0.1.0.jar --spring.profiles.active=prod
```

### Docker

```dockerfile
FROM openjdk:17-jdk-alpine
VOLUME /tmp
COPY target/eulen-spring-0.1.0.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
EXPOSE 8080
```

### Construcción Docker

```bash
docker build -t eulen-spring .
docker run -p 8080:8080 eulen-spring
```

## 📐 Convenciones de Código

### Nomenclatura

- **Packages**: lowercase (`com.ayesa.eulen.service`)
- **Classes**: PascalCase (`UserService`)
- **Methods**: camelCase (`getUserById`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)

### Code Style

- Utiliza Lombok para reducir boilerplate
- Implementa validación con Bean Validation
- Usa Optional para valores que pueden ser null
- Documenta con JavaDoc métodos públicos

### Ejemplo con Lombok

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {
    @Email
    @NotBlank
    private String email;
    
    @NotBlank
    @Size(min = 3, max = 100)
    private String name;
}
```

## 🔌 Integración

### Consumir API REST

```java
@Service
public class ExternalApiClient {
    
    @Autowired
    private RestTemplate restTemplate;
    
    public DataResponse fetchData() {
        return restTemplate.getForObject(
            "http://eulen-api:3000/api/v1/data",
            DataResponse.class
        );
    }
}
```

### Messaging con RabbitMQ

```java
@Configuration
public class RabbitConfig {
    
    @Bean
    public Queue queue() {
        return new Queue("eulen-queue", true);
    }
    
    @Bean
    public MessageConverter jsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }
}
```

## 🐛 Debugging

### Application Properties para Debug

```yaml
logging:
  level:
    com.ayesa.eulen: TRACE
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

### IntelliJ IDEA Debug Configuration

1. Run → Edit Configurations
2. Add New Configuration → Spring Boot
3. Main class: `com.ayesa.eulen.Application`
4. Use classpath of module: eulen-spring

## 📚 Recursos

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Security](https://docs.spring.io/spring-security/reference/)

## 👥 Equipo

**Owner**: team-eulen-backend

## 🔗 Enlaces

- [API Documentation](./api.md)
- [Architecture Overview](./index.md)
- [Jenkins Build](https://jenkins.ayesa.com/job/Eulen/job/spring-service-build)

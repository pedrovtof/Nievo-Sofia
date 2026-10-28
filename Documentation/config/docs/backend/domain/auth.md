# Auth Microservice Domain Models, Schemas & Services

## 1. Overview
The **Auth Microservice** is responsible for authentication, identity management, and credential verification within the Sofia ecosystem. This module defines the foundational communication schemas using Pydantic models, standardized API response envelopes, SQLAlchemy database session management, declarative ORM entities, persistence repositories, signup application services, custom logger wrappers, and unhandled exception middleware.

---

## 2. Architecture & Class Diagram

The following Mermaid class diagram illustrates the object hierarchy of the standard Pydantic response models, SQLAlchemy ORM entities, data access repository, database session manager, signup service components, logging subsystem, and exception handling middleware:

```mermaid
classDiagram
    direction TB

    class BaseApiResponse {
        <<model>>
        +Optional~str~ message
        +Optional~dict~ data
        +Optional~str~ status
    }

    class BaseApiSuccess {
        <<model>>
        +str message
        +str status
    }

    class BaseApiError {
        <<model>>
        +str message
        +str status
        +Optional~list~ errors
    }

    class Base {
        <<entity>>
    }

    class User {
        <<entity>>
        +UUID id
        +Optional~str~ full_name
        +Optional~str~ nick_name
        +Optional~str~ email
        +Optional~str~ phone
        +bool active
        +datetime created_at
        +datetime updated_at
        +__repr__() str
    }

    class SessionManager {
        <<service>>
        -Optional~Engine~ _engine
        -Optional~sessionmaker~ _session_factory
        +initialize(db_url: str, pool_size: int, max_overflow: int) void
        +get_db() Generator~Session~
        +get_session() Session
        +close() void
    }

    class UserRepository {
        <<repository>>
        +Session db
        +get_by_id(user_id: UUID) Optional~User~
        +get_by_mail(user_email: str) Optional~User~
        +create(user: User) User
        +update(user: User) User
    }

    class SignupUserRequest {
        <<model>>
        +EmailStr email
        +str password
        +bool accept_terms
    }

    class SignupService {
        <<service>>
        -UserRepository _user_repository
        +signup_user(request: SignupUserRequest) JSONResponse
    }

    class CustomLogger {
        <<service>>
        -Logger logger
        +debug(message: str) void
        +info(message: str) void
        +warning(message: str) void
        +error(message: str) void
        +critical(message: str) void
    }

    class ServerExceptionHandler {
        <<middleware>>
        +Request request
        +Exception exception
        +handle_exception() JSONResponse
    }

    BaseApiResponse <|-- BaseApiSuccess : Generalization
    BaseApiResponse <|-- BaseApiError : Generalization
    Base <|-- User : Generalization
    SignupService --> UserRepository : Depends on
    SignupService ..> SignupUserRequest : Consumes
    SignupService ..> BaseApiSuccess : Creates response payload
    UserRepository ..> SessionManager : Injects DB session
    UserRepository ..> User : Queries and persists
    ServerExceptionHandler ..> BaseApiError : Instantiates error payload
    ServerExceptionHandler ..> CustomLogger : Logs unhandled exception
```

---

## 3. Specifications & Schemas

### 3.1 Base API Response Schemas
All microservice endpoints adhere to a standardized JSON response envelope backed by Pydantic models:

- **[`BaseApiResponse`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_response.py)**:
  - `status`: String indicator (`"true"` or `"false"`).
  - `message`: User-friendly human-readable message.
  - `data`: Arbitrary dictionary payload containing response details.
  - Serialized via Pydantic `model_dump(mode="json")`.

- **[`BaseApiSuccess`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_sucess.py)**:
  - Extends `BaseApiResponse` with default values: `status="true"`, `message="executed with success"`.

- **[`BaseApiError`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_error.py)**:
  - Extends `BaseApiResponse` with default values: `status="false"`, `message="An error occurred"`.
  - Additional field `errors`: List of validation or domain error strings.

### 3.2 Database Session Management & ORM Persistence
- **[`SessionManager`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/database/session_manager.py)**:
  - Manages the SQLAlchemy `Engine` connection pool (`pool_pre_ping=True`, configurable `pool_size` and `max_overflow`) and `sessionmaker` lifecycle.
  - Initialized during FastAPI `lifespan` startup via `PGSQL_DATABASE_PLATFORM_AUTH_ACCOUNTS_CONNECTION_STRING` and disposed gracefully on shutdown.
  - Exposes `get_db()` generator dependency for FastAPI routes with automatic rollback on unhandled exceptions and deterministic session cleanup.
- **[`Base`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/contracts/entities/model.py)** & **[`User`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/contracts/entities/user.py)**:
  - SQLAlchemy 2.0 `DeclarativeBase` and `User` entity mapped to `member.user` with UUIDv7 primary key generation (`id`), profile attributes (`full_name`, `nick_name`, `email`, `phone`), `active` status flag, and audit timestamps (`created_at`, `updated_at`).
- **[`UserRepository`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/user.py)**:
  - Encapsulates data access operations against `member.user` using an injected SQLAlchemy `Session`: `get_by_id`, `get_by_mail`, `create`, and `update` with transactional rollback protection.

### 3.3 Signup Domain Service & Validation
- **[`SignupUserRequest`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/request.py)**:
  - Validates `email` as a valid email address via `EmailStr`.
  - Restricts `password` between 6 and 20 characters.
  - Requires explicit boolean confirmation for `accept_terms`.
- **[`SignupService`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/service.py)**:
  - Receives an injected `UserRepository` dependency via FastAPI `Depends`.
  - Executes `signup_user(request)` and returns an HTTP 202 Accepted envelope.

### 3.4 Core Logging Subsystem
- **[`CustomLogger`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/logging.py)**:
  - Encapsulates Python's native `logging.Logger`.
  - Configured with default timestamp format `YYYY-MM-DD HH:MM:SS` and log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

### 3.5 Server Exception Handler
- **[`ServerExceptionHandler`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/middleware/server_exception_handler.py)**:
  - Intercepts unexpected runtime exceptions during HTTP request lifecycle.
  - Records error logs using `CustomLogger.error(...)` including request method and URL.
  - Generates a structured HTTP 500 JSON response utilizing `BaseApiError`. Exception details are sanitized and only included in payload when `DEBUG="True"`.

---

## 4. Related Implementation Files
- [`base_api_response.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_response.py)
- [`base_api_sucess.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_sucess.py)
- [`base_api_error.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_error.py)
- [`session_manager.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/database/session_manager.py)
- [`model.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/contracts/entities/model.py)
- [`user.py` (Entity)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/contracts/entities/user.py)
- [`user.py` (Repository)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/user.py)
- [`request.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/request.py)
- [`service.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/service.py)
- [`controller.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/controller.py)
- [`logging.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/logging.py)
- [`server_exception_handler.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/middleware/server_exception_handler.py)
- [`main.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/main.py)

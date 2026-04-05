# AGENTS.md - Spectrum: Symbolic Regression Platform

**System Instruction**: You are operating withing a strict Domain-Driven Design (DDD) FastAPI codebase. This document outlines the immutable architectural boundaries, patterns and known gotchas of this project. Read carefully before proposing any code changes.

## Project & Stack Overview

**Purpose**: Web platform for executing and managing symbolic regression algorithms.
**Core Stack**: Python 3.12, FastAPI, PostgreSQL (asyncpg), SQLAlchemy 2.0 (async), RabbitMQ (aio_pika), Pydantic v2, uv (package manager).
**Architectural Style**: Clean Architecture / Domain-Driven Design (DDD) utilizing the Unit of Work, Repository, and Data Mapper patterns.

## Strict Architectural Boundaries

### Layer Isolation (Non-negotiable)

1. **Domain Layer** (core/): Contains pydantic models representing the core business entities and implementation interfaces. No external dependencies allowed.
2. **Database Layer** (db_core/): Contains SQLAlchemy models, database connection management, repository implementations and data mappers. Depends on the Domain Layer but must not contain any business logic.
3. **Application Layer** (backend/app/features): Contains FastAPI route handlers, services, and application logic. Depends on both the Domain and Database Layers but must not contain any direct database access code.
4. **Presentation Layer** (frontend/): React-based UI that interacts with the FastAPI backend via RESTful APIs. No direct access to the Domain or Database layers.

### Implementation Patterns

- **Data Mapper Pattern**: ORM models MUST NOT contain transformation logic. Use dedicated Mapper classes to translate between Domain models and Database models.
- **Protected Base Repository**: SqlAlchemyBaseRepository contains all raw DB I/O using protected methods (_add,_get_unique,_paginate_query). Concrete repositories (e.g., SqlAlchemyUsersRepository) implement specific Domain interfaces (IUsersRepository) by calling these protected helpers.
- **Unit of Work (UoW)**: All database mutations MUST happen within the ApiUnitOfWork context manager. The commit happens automatically on scope exit, ensuring transactional integrity.

## Database & SQLAlchemy 2.0 Rules

- **Async Only**: All database interactions MUST use async SQLAlchemy 2.0 patterns. Synchronous code is strictly prohibited.
- **Primary Key Lookups**: Use await session.get(Model, ident) ONLY for primary keys. For unique constraints (like email), use a select().where() query.
- **Cascades**: cascade="all, delete-orphan" MUST be placed on the Parent side of a one-to-many relationship. Never place it on the Many/Child side.
- **JSON Columns**: Always use PostgreSQL's JSONB type from sqlalchemy.dialects.postgresql instead of generic JSON to ensure .distinct() and equality operators work during pagination.
- **Deleting Transients**: If deleting an entity created in memory, you must attach it to the session first: tracked = await session.merge(orm); await session.delete(tracked).

## FastAPI & Pydantic v2 Rules

- **Pydantic Discriminated Unions**: When using polymorphic schemas (e.g., MarkdownBlock vs InferenceBlock), the discriminator field MUST be strictly typed using typing.Literal (e.g., kind: Literal[BlockKind.MARKDOWN] = BlockKind.MARKDOWN). Remove the discriminator field from the Base class to avoid type-checker invariance errors.
- **Response Models**: Ensure the @router.get(response_model=...) strictly matches the return type. If returning paginated data, use response_model=PaginatedResponse[JobDto], not list[Job].
- **SecretStr**: When validating SecretStr fields (like passwords), you MUST call .get_secret_value() to perform string checks, but always return the wrapped SecretStr object from the validator.
- **Global State**: Prevent circular imports by storing global connections (like RabbitMQ aio_pika channels) in a dedicated state.py file, rather than attaching them to app.state inside main.py.

## File System & Security

- **Pathlib**: When joining user-provided paths to a base directory via pathlib.Path, ALWAYS strip leading slashes (user_path.lstrip("/")) to prevent the root path from being overwritten.
- **Traversal Protection**: Always use .resolve().is_relative_to(base_dir) to prevent path traversal attacks before writing files to local storage.
- **Auth**: JWT tokens are stored in HttpOnly cookies, not JSON response bodies, to prevent XSS.

## Agent Workflow Rules

- **No blind coding**: Propose architectural changes or complex ORM relationships before writing the full implementation.
- **Update this file**: If a new framework quirk, circular import, or structural rule is established during the conversation, suggest adding it to this AGENTS.md document.

## Coding Style & Conventions

### Naming Conventions (Strict)

- **Domain Entities**: Pure, un-suffixed nouns (e.g., User, Job, Run, Block).
- **Database Models**: Must end with ORM (e.g., UserORM, JobORM).
- **Data Transfer Objects (Schemas)**: Must end with Dto (e.g., CreateUserDto, BulkUpdateBlockDto).
- **Interfaces/Protocols**: Must be prefixed with an uppercase I (e.g., IUsersRepository, IUnitOfWork).
- **Concrete Implementations**: Prefixed with the technology used (e.g., SqlAlchemyUsersRepository, AioPikaBroker).
- **Protected Methods**: Any helper method inside a base class that should not be exposed to the public API must start with an underscore (e.g., self._get_unique()).

### Type Hinting (Python 3.13+)

- **Zero Any Tolerance**: Do not use Any unless integrating with an untyped third-party library.
**Modern Generics**: Use Python 3.12+ syntax for generics where applicable (e.g., class BaseBlock[T](BaseModel):).
**Dependency Injection**: Rely heavily on typing.Protocol to define contracts for Services and Repositories so the API layer never imports concrete database classes.

### Asynchronous Programming

- **Non-Blocking I/O**: Never use synchronous blocking functions (like time.sleep() or standard open()) inside an async def FastAPI route. Use await asyncio.sleep() or offload heavy disk/CPU tasks (like hashing large dataset files) to a threadpool (e.g., fastapi.concurrency.run_in_threadpool).
- **Concurrency**: Use asyncio.gather() when making multiple independent database calls or external requests to optimize response times.
- **Error Handling & Exceptions**: No Raw HTTP Exceptions in Domain: The Domain and Service layers must raise custom Python exceptions (e.g., JobNotFound, InvalidIQLSyntax).
- **Exception Mapping**: The FastAPI Router layer (or global exception handlers in main.py) is solely responsible for catching these custom exceptions and translating them into standard fastapi.HTTPException responses (400, 401, 404, etc.).

### Code Formatting

- **Ruff**: All code is formatted and linted using ruff. The agent must output code that adheres to standard PEP 8 line lengths and avoids unused imports.

## Event Publishing & RabbitMQ (aio_pika)

- **Transaction Safety:** NEVER publish a RabbitMQ event before the SQLAlchemy Unit of Work has successfully committed. If the DB transaction rolls back, the event must not be fired.
- **Broker Injection:** Do not instantiate `aio_pika` connections inside services. The `AioPikaBroker` (or `IMessageBroker` interface) must be injected into the Service or Unit of Work.
- **Exchange Naming:** Always use explicitly named exchanges (e.g., `MAIN_EXCHANGE_NAME = "spectrum_events"`). Never attempt to configure or declare the default empty string exchange (`""`), as RabbitMQ will throw an `ACCESS_REFUSED` error.
- **Queue Separation:** Dedicated tasks (e.g., training vs. inference) MUST use separate queues to allow for independent scaling and priority management (e.g., `workers.training`, `workers.inference`).
- **Handler Isolation:** Each worker queue should have its own set of `EventHandler` implementations, registered within the main consumer loop.

## Domain Logic & IQL Handling

- **IQL Isolation:** Any parsing, validation, or manipulation of IQL (your symbolic regression domain language) belongs strictly inside the pure Python Domain Layer.
- **No Leaks:** FastAPI routers and Pydantic DTOs must treat IQL expressions as opaque strings. They pass the string down to the Domain/Service layer, which is responsible for ensuring the expression is valid, calculating `max_size`, or applying simplifications.

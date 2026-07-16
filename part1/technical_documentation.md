# HBnB Evolution – Technical Documentation

## Introduction

This document describes the technical architecture and design of the HBnB Evolution application.

The project is organized into progressive phases:

- Part 1: Technical documentation and UML design
- Part 2: Business logic and REST API
- Part 3: Authentication, authorization, and database persistence
- Part 4: Simple browser-based web client

The application follows a layered architecture designed to separate HTTP handling, business operations, persistence, and database storage.

---

# 1. High-Level Architecture

## Source Diagram

[View High-Level Architecture Source](./high-level-diagram.mmd)

## Rendered Diagram

![High-Level Architecture](./high-level-diagram.mmd.svg)

## Architecture Layers

The HBnB application contains four logical layers:

1. Presentation Layer
2. Business Logic Layer
3. Persistence Layer
4. Database Layer

---

## Presentation Layer

The presentation layer exposes the HBnB REST API using Flask and Flask-RESTX.

### Components

- User API endpoints
- Place API endpoints
- Review API endpoints
- Amenity API endpoints
- Authentication API endpoint
- Browser-based web client

### Responsibilities

- Receive HTTP requests
- Validate request data
- Process authentication tokens
- Call facade operations
- Return JSON responses
- Provide API documentation
- Display data in the browser client

---

## Business Logic Layer

The business logic layer contains the application's core entities and coordinates application operations.

### Components

- `HBnBFacade`
- `BaseModel`
- `User`
- `Place`
- `Review`
- `Amenity`

### Responsibilities

- Create and retrieve entities
- Apply business rules
- Verify related entities exist
- Coordinate repositories
- Prevent direct coupling between the API and persistence layers

---

## Persistence Layer

The persistence layer encapsulates data access through the Repository pattern.

### Components

- `Repository`
- `InMemoryRepository`
- `SQLAlchemyRepository`
- `UserRepository`
- `PlaceRepository`
- `ReviewRepository`
- `AmenityRepository`

### Responsibilities

- Add entities
- Retrieve entities by ID
- Retrieve all entities
- Update entities
- Delete entities
- Query entities by attributes
- Commit database changes

---

## Database Layer

The database layer stores persistent application data using SQLite during development.

SQLAlchemy maps Python entities to the following relational tables:

- `users`
- `places`
- `reviews`
- `amenities`
- `place_amenity`

The `place_amenity` table implements the many-to-many relationship between places and amenities.

---

## Facade Pattern

The system uses the Facade pattern through `HBnBFacade`.

The facade provides one interface between the presentation layer and the repositories.

### Communication Flow

```text
Client or Browser
        |
        v
Flask REST API
        |
        v
HBnBFacade
        |
        v
Repositories
        |
        v
Database
```

### Benefits

- Reduces coupling
- Centralizes application operations
- Simplifies API endpoint code
- Makes persistence implementations replaceable
- Improves maintainability and testing

---

# 2. Business Logic Layer

## Source Diagram

[View Business Logic Diagram Source](./business-logic-layer.mmd)

## Rendered Diagram

![Business Logic Diagram](./business-logic-layer.mmd.svg)

---

## BaseModel

### Purpose

Provides attributes and behavior shared by all entities.

### Attributes

- `id : UUID`
- `created_at : datetime`
- `updated_at : datetime`

### Methods

- `update(data)`
- `to_dict()`

---

## User

### Purpose

Represents a user of the HBnB application.

### Attributes

- `first_name : String`
- `last_name : String`
- `email : String`
- `password : String`
- `is_admin : Boolean`

### Methods

- `hash_password(password)`
- `verify_password(password)`
- `to_dict()`

### Relationships

- One user can own zero or many places.
- One user can write zero or many reviews.

---

## Place

### Purpose

Represents a property listed in HBnB.

### Attributes

- `title : String`
- `description : String`
- `price : Float`
- `latitude : Float`
- `longitude : Float`
- `owner_id : UUID`

### Methods

- `add_amenity(amenity)`
- `to_dict()`

### Relationships

- Each place belongs to one user.
- One place can receive zero or many reviews.
- One place can contain zero or many amenities.

---

## Review

### Purpose

Represents textual feedback submitted by a user for a place.

### Attributes

- `text : String`
- `user_id : UUID`
- `place_id : UUID`

### Methods

- `to_dict()`

### Relationships

- Each review belongs to one user.
- Each review belongs to one place.

---

## Amenity

### Purpose

Represents a feature or service associated with a place.

Examples include:

- WiFi
- Swimming pool
- Air conditioning
- Parking

### Attributes

- `name : String`

### Methods

- `to_dict()`

### Relationships

- One amenity can be associated with zero or many places.
- One place can contain zero or many amenities.

---

## Entity Relationships

### Inheritance

```text
BaseModel
 ├── User
 ├── Place
 ├── Review
 └── Amenity
```

### User and Place

```text
User 1 -------- 0..* Place
```

A user can own multiple places. Each place has one owner.

### User and Review

```text
User 1 -------- 0..* Review
```

A user can write multiple reviews. Each review has one author.

### Place and Review

```text
Place 1 -------- 0..* Review
```

A place can receive multiple reviews. Each review references one place.

### Place and Amenity

```text
Place 0..* -------- 0..* Amenity
```

This relationship is implemented through the `place_amenity` association table.

---

# 3. API Interaction Sequences

The sequence diagrams show how requests move through the presentation, business logic, persistence, and database layers.

---

## 3.1 User Registration

### Source Diagram

[View User Registration Sequence](./User-Registration-Sequence.mmd)

### Rendered Diagram

![User Registration Sequence](./User-Registration-Sequence.mmd.svg)

### Flow

1. The client submits user registration data.
2. The API validates the request.
3. The facade checks whether the email already exists.
4. The password is hashed.
5. A `User` entity is created.
6. The repository stores the user.
7. The API returns a sanitized response without the password.

---

## 3.2 Place Creation

### Source Diagram

[View Place Creation Sequence](./Place-Creation-Sequence.mmd)

### Rendered Diagram

![Place Creation Sequence](./Place-Creation-Sequence.mmd.svg)

### Flow

1. The authenticated client submits place data.
2. The API validates the request and JWT.
3. The authenticated user is identified.
4. The facade creates a `Place`.
5. The repository persists the place.
6. The API returns the created place.

---

## 3.3 Review Submission

### Source Diagram

[View Review Submission Sequence](./Review-Submission-Sequence.mmd)

### Rendered Diagram

![Review Submission Sequence](./Review-Submission-Sequence.mmd.svg)

### Flow

1. The authenticated user submits review text.
2. The API validates the JWT and request data.
3. The place is verified.
4. The authenticated user is identified.
5. The facade creates a `Review`.
6. The repository persists the review.
7. The API returns the created review.

---

## 3.4 Fetching the Places List

### Source Diagram

[View Places List Sequence](./Fetching-Places-List-Sequence.mmd)

### Rendered Diagram

![Fetching Places List Sequence](./Fetching-Places-List-Sequence.mmd.svg)

### Flow

1. The client requests the list of places.
2. The API calls the facade.
3. The facade queries the place repository.
4. SQLAlchemy retrieves the records.
5. The API returns the list as JSON.
6. The browser client dynamically creates place cards.

---

# 4. Authentication and Authorization

The HBnB backend uses JSON Web Tokens for authentication.

## Login Process

1. The client submits an email and password.
2. The API retrieves the user by email.
3. Bcrypt verifies the password.
4. The API generates a JWT access token.
5. The browser stores the token in a cookie.
6. Protected requests send the token in the `Authorization` header.

## Administrative Access

JWT claims include the user's administrator status.

Administrator-only operations can inspect the `is_admin` claim before allowing access.

## Password Protection

Passwords are hashed using Bcrypt before storage.

Passwords are never returned by user serialization methods or GET endpoints.

---

# 5. Database Design

The relational schema contains five tables.

## Users

Stores user identity, authentication, and administrator information.

## Places

Stores property information and references the owner through `owner_id`.

## Reviews

Stores review text and references both a user and a place.

## Amenities

Stores available feature names.

## Place Amenity

Links places and amenities through a composite primary key.

See the Part 3 database diagram for the complete entity-relationship model.

---

# 6. Design Patterns

## Application Factory Pattern

The Flask application is created by `create_app()`.

This allows configuration classes to be selected for development, testing, or production.

## Facade Pattern

`HBnBFacade` centralizes communication between API endpoints, models, and repositories.

## Repository Pattern

Repositories isolate database operations from business and presentation code.

## Object-Oriented Inheritance

All business entities inherit shared identifiers and timestamps from `BaseModel`.

## ORM Mapping

SQLAlchemy maps Python classes and relationships to relational database tables.

---

# 7. Web Client

Part 4 implements a browser-based client using:

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- Cookies

The client includes:

- Login page
- Places list
- Price filtering
- Place-details page
- Add-review form
- JWT-based authenticated requests

The frontend communicates with the Part 3 Flask API.

---

# 8. Security Considerations

The architecture supports:

- Bcrypt password hashing
- JWT authentication
- Administrator claims
- Ownership checks
- Input validation
- Unique email constraints
- Foreign-key relationships
- CORS configuration
- Password exclusion from responses

Authorization rules must be enforced by the backend and must not rely only on browser-side JavaScript.

---

# Conclusion

The HBnB architecture separates presentation, business logic, persistence, and database concerns.

The documentation and diagrams describe:

- the high-level application structure;
- the business entities;
- entity relationships;
- database persistence;
- authentication;
- API interaction flows;
- browser-client integration.

This design provides a clear foundation for maintaining and extending the HBnB application.

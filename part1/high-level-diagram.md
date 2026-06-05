# HBnB - High Level Package Diagram

## Objective

This diagram illustrates the three-layer architecture of the HBnB application and the communication flow between layers using the Facade Pattern.

---

## Architecture Overview

The application is divided into three layers:

### 1. Presentation Layer

The Presentation Layer is responsible for interacting with users and external clients.

Components:

* API
* Services

Responsibilities:

* Receive requests
* Validate input
* Return responses
* Delegate operations to the facade

---

### 2. Business Logic Layer

The Business Logic Layer contains the application's core rules and entities.

Components:

* HBnBFacade
* User
* Place
* Review
* Amenity

Responsibilities:

* Implement business rules
* Coordinate system operations
* Validate domain logic
* Interact with repositories

The HBnBFacade acts as the single entry point to this layer.

---

### 3. Persistence Layer

The Persistence Layer manages data storage and retrieval.

Components:

* UserRepository
* PlaceRepository
* ReviewRepository
* AmenityRepository

Responsibilities:

* Database operations
* Data persistence
* Query execution
* Data retrieval

---

## Facade Pattern

The HBnBFacade simplifies communication between the Presentation Layer and the Business Logic Layer.

Benefits:

* Reduces coupling between layers
* Hides internal complexity
* Provides a unified interface
* Improves maintainability

Communication Flow:

Presentation Layer → HBnBFacade → Business Logic Layer → Persistence Layer

The Presentation Layer never communicates directly with repositories or database components.

---

## SOLID Principles Applied

### Single Responsibility Principle (SRP)

Each layer has a specific responsibility:

* Presentation handles requests.
* Business Logic handles domain rules.
* Persistence handles data storage.

### Open/Closed Principle (OCP)

New entities or services can be added without modifying existing components.

### Liskov Substitution Principle (LSP)

Repositories can be replaced by alternative implementations while maintaining behavior.

### Interface Segregation Principle (ISP)

The facade exposes only the operations needed by the Presentation Layer.

### Dependency Inversion Principle (DIP)

Business logic depends on abstractions (repositories) rather than concrete database implementations.

---

## Conclusion

The HBnB architecture follows a layered design that promotes separation of concerns, maintainability, and scalability. The Facade Pattern provides a clean communication mechanism between layers while supporting SOLID object-oriented design principles.


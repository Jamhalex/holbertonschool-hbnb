#  Sequence Diagrams for API Calls

## Overview

This document explains the sequence diagrams created for the HBnB Evolution application. These diagrams illustrate how the Presentation Layer, Business Logic Layer, and Persistence Layer interact to process different API requests.

The diagrams demonstrate the flow of information between components and highlight the role of the Facade Pattern in coordinating communication between layers.

---

# 1. User Registration

## Description

This sequence diagram represents the process of registering a new user in the system.

The user submits registration information through the API. The request is passed to the Facade, which coordinates validation and user creation. Once the data is validated, the user is stored in the database and a success response is returned.

## Flow of Interactions

1. The user sends a registration request.
2. The API receives the request.
3. The API forwards the request to the Facade.
4. The Facade validates the user data through the User model.
5. The user information is saved in the database.
6. The database confirms successful storage.
7. The Facade returns a success response.
8. The API returns a confirmation to the user.

## Purpose

The diagram demonstrates how new users are added to the system while maintaining separation of concerns between layers.

---

# 2. Place Creation

## Description

This sequence diagram illustrates how a user creates a new place listing.

The API receives place information and forwards it to the Facade. The Place model validates the data before it is persisted in the database.

## Flow of Interactions

1. The user submits place information.
2. The API receives the request.
3. The API calls the Facade.
4. The Facade validates the place data through the Place model.
5. The place is stored in the database.
6. The database confirms successful creation.
7. The Facade returns a success response.
8. The API sends confirmation back to the user.

## Purpose

The diagram shows how property listings are created and stored while ensuring business rules are enforced before persistence.

---

# 3. Review Submission

## Description

This sequence diagram represents the process of submitting a review for a place.

The review information is received by the API, validated by the Review model through the Facade, and then stored in the database.

## Flow of Interactions

1. The user submits a review.
2. The API receives the request.
3. The request is forwarded to the Facade.
4. The Review model validates the review data.
5. The review is saved in the database.
6. The database confirms successful storage.
7. The Facade returns a success response.
8. The API responds to the user.

## Purpose

The diagram demonstrates how user feedback is processed and associated with places within the system.

---

# 4. Fetching a List of Places

## Description

This sequence diagram illustrates how a user retrieves a list of available places.

The API receives the request, the Facade queries the database, and the resulting data is returned to the user.

## Flow of Interactions

1. The user requests a list of places.
2. The API receives the request.
3. The API forwards the request to the Facade.
4. The Facade queries the database.
5. The database returns the matching places.
6. The Place model formats the results if necessary.
7. The Facade prepares the response.
8. The API returns the list of places to the user.

## Purpose

The diagram shows the retrieval process and demonstrates how data flows from storage to presentation.

---

# Layer Responsibilities

## Presentation Layer

The Presentation Layer serves as the entry point to the application.

### Responsibilities

* Receive HTTP requests.
* Validate request format.
* Forward requests to the Business Logic Layer.
* Return HTTP responses to clients.

### Components

* API Endpoints
* Services

---

## Business Logic Layer

The Business Logic Layer contains the application's core rules and behavior.

### Responsibilities

* Validate business data.
* Execute business operations.
* Coordinate interactions between entities.
* Communicate with the Persistence Layer.

### Components

* Facade
* User Model
* Place Model
* Review Model
* Amenity Model

---

## Persistence Layer

The Persistence Layer manages data storage and retrieval.

### Responsibilities

* Store application data.
* Retrieve records from the database.
* Ensure data consistency.

### Components

* Database
* Repositories
* Data Access Objects (DAO)

---

# Facade Pattern

The Facade Pattern acts as a unified interface between the Presentation Layer and the Business Logic Layer.

Instead of allowing API endpoints to communicate directly with multiple models, the API interacts only with the Facade. The Facade coordinates the required operations and delegates responsibilities to the appropriate business entities.

## Benefits

* Reduces coupling between layers.
* Simplifies communication.
* Improves maintainability.
* Promotes a cleaner architecture.
* Provides a single entry point to business operations.

---

# Conclusion

The sequence diagrams provide a clear representation of how requests flow through the HBnB Evolution architecture. They demonstrate the responsibilities of each layer and show how the Facade Pattern simplifies communication between components while preserving a clean and maintainable system design.


# HBnB Evolution - Technical Documentation

## Introduction

This document provides the technical design and architecture of the HBnB Evolution application. It serves as a blueprint for the implementation phases by describing the system architecture, business logic entities, and API interaction flows.

HBnB Evolution is a simplified Airbnb-like platform that allows users to register, manage places, submit reviews, and associate amenities with places. The application follows a layered architecture composed of Presentation, Business Logic, and Persistence layers.

---

# 1. High-Level Architecture

## Purpose

The purpose of this diagram is to illustrate the overall architecture of the HBnB application and the communication between layers using the Facade Pattern.

## High-Level Package Diagram

![High-Level Package Diagram](task0_package_diagram.png)

### Architecture Overview

The system is divided into three layers:

### Presentation Layer

Responsible for handling user interactions through API endpoints and services.

Components:

- REST API
- Services
- Controllers

### Business Logic Layer

Contains the core domain models and business rules.

Entities:

- User
- Place
- Review
- Amenity

The Facade acts as a unified interface between the Presentation Layer and the Business Logic Layer.

### Persistence Layer

Responsible for storing and retrieving data.

Components:

- Repository Layer
- Database Access Objects
- Database

### Facade Pattern

The Facade Pattern simplifies communication between layers by exposing a single interface to the Presentation Layer. This reduces coupling and centralizes business operations.

---

# 2. Business Logic Layer

## Purpose

This diagram represents the internal structure of the Business Logic Layer, including entities, attributes, methods, and relationships.

## Detailed Class Diagram

![Business Logic Diagram](task1_class_diagram.png)

---

## BaseModel

### Role

Parent class for all entities.

### Attributes

- id : UUID
- created_at : datetime
- updated_at : datetime

### Methods

- save()
- update()
- delete()

---

## User

### Role

Represents platform users.

### Attributes

- first_name
- last_name
- email
- password
- is_admin

### Methods

- register()
- update_profile()
- delete()

---

## Place

### Role

Represents a property listed by a user.

### Attributes

- title
- description
- price
- latitude
- longitude

### Methods

- create()
- update()
- delete()

---

## Review

### Role

Represents a user review of a place.

### Attributes

- rating
- comment

### Methods

- create()
- update()
- delete()

---

## Amenity

### Role

Represents features available in a place.

### Attributes

- name
- description

### Methods

- create()
- update()
- delete()

---

## Relationships

### User → Place

A User can own multiple Places.

Multiplicity:

```text
User 1 ---- 0..* Place
```

### User → Review

A User can write multiple Reviews.

Multiplicity:

```text
User 1 ---- 0..* Review
```

### Place → Review

A Place can receive multiple Reviews.

Multiplicity:

```text
Place 1 ---- 0..* Review
```

### Place ↔ Amenity

Many-to-Many relationship.

Multiplicity:

```text
Place 0..* ---- 0..* Amenity
```

### Inheritance

All entities inherit from BaseModel.

---

# 3. API Interaction Flow

The following sequence diagrams illustrate how requests travel through the Presentation, Business Logic, and Persistence layers.

---

## 3.1 User Registration

![User Registration](user_registration.png)

### Description

This sequence demonstrates the registration of a new user.

### Flow

1. User submits registration data.
2. API validates request.
3. Facade creates User object.
4. Repository persists data.
5. Database stores record.
6. Success response is returned.

---

## 3.2 Place Creation

![Place Creation](place_creation.png)

### Description

This sequence demonstrates how a user creates a new property listing.

### Flow

1. User submits place information.
2. API forwards request.
3. Facade validates ownership.
4. Place object is created.
5. Repository stores place.
6. Success response is returned.

---

## 3.3 Review Submission

![Review Submission](review_submission.png)

### Description

This sequence demonstrates how a review is added to a place.

### Flow

1. User submits review.
2. API validates request.
3. Facade verifies user and place.
4. Review object is created.
5. Repository saves review.
6. Success response is returned.

---

## 3.4 Fetch Places

![Fetch Places](fetch_places.png)

### Description

This sequence demonstrates retrieving a list of places.

### Flow

1. User requests places.
2. API forwards query.
3. Facade requests data.
4. Repository retrieves records.
5. Database returns places.
6. API returns results.

---

# Conclusion

This document provides the architectural foundation of the HBnB Evolution project. The package diagram defines the layered architecture and Facade Pattern, the class diagram specifies the business entities and relationships, and the sequence diagrams describe the interaction flow of key API operations. Together, these diagrams serve as a guide for the implementation phases of the application.

# Detailed Class Diagram for the Business Logic Layer

## Overview

The Business Logic Layer contains the core entities and rules of the HBnB application. These entities model the application's main concepts and define how data is organized and manipulated.

To promote code reuse and maintainability, all entities inherit from a common `BaseModel` class that provides shared attributes and behavior.

---

# Entities

## BaseModel

The `BaseModel` class serves as the parent class for all business entities.

### Responsibilities

- Provide a unique identifier for every object.
- Store creation and update timestamps.
- Provide shared update behavior.
- Provide dictionary serialization.

### Attributes

- `id : UUID`
- `created_at : datetime`
- `updated_at : datetime`

### Methods

- `update(data)`
- `to_dict()`

---

## User

The `User` entity represents a person who interacts with the application.

Users can own places, write reviews, authenticate with a password, and may have administrator privileges.

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

### Responsibilities

- Store user information.
- Own places.
- Write reviews.
- Authenticate securely.
- Access privileged operations when marked as an administrator.

---

## Place

The `Place` entity represents a property listed on the platform.

Each place belongs to one user and can be associated with multiple reviews and amenities.

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

### Responsibilities

- Store property information.
- Reference its owner.
- Associate amenities with the property.
- Receive reviews from users.

---

## Review

The `Review` entity represents textual feedback provided by a user about a place.

### Attributes

- `text : String`
- `user_id : UUID`
- `place_id : UUID`

### Methods

- `to_dict()`

### Responsibilities

- Store textual feedback.
- Reference the user who wrote the review.
- Reference the place being reviewed.

---

## Amenity

The `Amenity` entity represents a service or feature available at a place.

Examples include WiFi, parking, a swimming pool, or air conditioning.

### Attributes

- `name : String`

### Methods

- `to_dict()`

### Responsibilities

- Describe a feature or service.
- Be associated with one or more places.

---

# Relationships Between Entities

## User and Place

A user can own zero or many places, while each place belongs to exactly one user.

### Multiplicity

```text
User 1 -------- 0..* Place

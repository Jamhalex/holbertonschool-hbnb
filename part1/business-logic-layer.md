#  Detailed Class Diagram for Business Logic Layer

## Overview

The Business Logic Layer contains the core entities and rules of the HBnB Evolution application. These entities model the application's main concepts and define how data is organized and manipulated within the system.

To promote code reuse and maintainability, all entities inherit from a common `BaseModel` class that provides shared attributes and behaviors.

---

# Entities

## BaseModel

The `BaseModel` class serves as the parent class for all business entities.

### Responsibilities

* Provide a unique identifier for every object.
* Store creation and update timestamps.
* Define common operations shared by all entities.

### Attributes

* `id : UUID`
* `created_at : datetime`
* `updated_at : datetime`

### Methods

* `save()`
* `update()`
* `delete()`

---

## User

The `User` entity represents a person who interacts with the application.

Users can create places, write reviews, and may have administrator privileges.

### Attributes

* `first_name : String`
* `last_name : String`
* `email : String`
* `password : String`
* `is_admin : Boolean`

### Methods

* `register()`
* `update_profile()`

### Responsibilities

* Manage user information.
* Own places.
* Submit reviews.
* Access system features according to permissions.

---

## Place

The `Place` entity represents a property listed on the platform.

Each place belongs to a specific user and can contain multiple amenities.

### Attributes

* `title : String`
* `description : String`
* `price : Float`
* `latitude : Float`
* `longitude : Float`

### Methods

* `add_amenity()`
* `remove_amenity()`

### Responsibilities

* Store property information.
* Associate amenities with the property.
* Receive reviews from users.

---

## Review

The `Review` entity represents feedback provided by a user about a place.

### Attributes

* `rating : Integer`
* `comment : String`

### Methods

* `edit_review()`

### Responsibilities

* Store user evaluations.
* Associate users with places through feedback.
* Provide quality and reputation information about places.

---

## Amenity

The `Amenity` entity represents a service or feature available in a place.

Examples include Wi-Fi, parking, swimming pool, or air conditioning.

### Attributes

* `name : String`
* `description : String`

### Methods

* `update_amenity()`

### Responsibilities

* Describe available services.
* Be associated with one or more places.

---

# Relationships Between Entities

## User and Place

A user can own multiple places, but each place has only one owner.

### Multiplicity

```text
User 1 -------- * Place
```

This relationship represents ownership.

---

## User and Review

A user can write multiple reviews.

### Multiplicity

```text
User 1 -------- * Review
```

This relationship represents authorship.

---

## Place and Review

A place can receive multiple reviews.

### Multiplicity

```text
Place 1 -------- * Review
```

This relationship represents customer feedback associated with a property.

---

## Place and Amenity

A place can contain multiple amenities, and an amenity can belong to multiple places.

### Multiplicity

```text
Place * -------- * Amenity
```

This is a many-to-many relationship.

Examples:

* One place may have Wi-Fi, parking, and a pool.
* Wi-Fi may exist in many different places.

---

# Design Considerations

The diagram follows Object-Oriented Programming principles and promotes code reuse through inheritance.

The use of `BaseModel` avoids duplication of common attributes and behaviors across entities.

The relationships accurately reflect the business requirements of the HBnB Evolution application and provide a clear foundation for future implementation in subsequent project phases.

---

# UML Concepts Used

* **Classes** represent business entities.
* **Inheritance** is used through `BaseModel`.
* **Associations** represent interactions between entities.
* **Multiplicity** specifies how many objects participate in each relationship.
* **Encapsulation** groups data and behavior within each entity.

This design provides a maintainable, scalable, and organized structure for the Business Logic Layer of the HBnB Evolution application.


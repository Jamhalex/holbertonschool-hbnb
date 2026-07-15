# HBnB Database Entity-Relationship Diagram

This document represents the HBnB relational database schema and the relationships between users, places, reviews, amenities, and the place-amenity association table.

```mermaid
erDiagram
    USERS {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(50) first_name
        VARCHAR(50) last_name
        VARCHAR(120) email UK
        VARCHAR(255) password
        BOOLEAN is_admin
    }

    PLACES {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(100) title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        VARCHAR(36) owner_id FK
    }

    REVIEWS {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        TEXT text
        VARCHAR(36) user_id FK
        VARCHAR(36) place_id FK
    }

    AMENITIES {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(50) name UK
    }

    PLACE_AMENITY {
        VARCHAR(36) place_id PK, FK
        VARCHAR(36) amenity_id PK, FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES ||--o{ PLACE_AMENITY : has
    AMENITIES ||--o{ PLACE_AMENITY : assigned_to
```

## Relationship Summary

A user can own zero or many places, while each place belongs to exactly one user.

A user can write zero or many reviews, while each review belongs to exactly one user.

A place can receive zero or many reviews, while each review belongs to exactly one place.

Places and amenities have a many-to-many relationship. The `PLACE_AMENITY` association table links places to amenities using a composite primary key containing `place_id` and `amenity_id`.

## Constraints

* Every table uses a UUID string as its primary key.
* User email addresses must be unique.
* Amenity names must be unique.
* Every place must reference an existing user through `owner_id`.
* Every review must reference an existing user and place.
* Each place and amenity combination can appear only once in `PLACE_AMENITY`.


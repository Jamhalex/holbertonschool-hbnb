# HBnB Part 1 UML

This folder contains the UML diagrams for the HBnB project and the script to regenerate PNG exports.

## Business rules summary

- Users can register, authenticate, and manage their profiles.
- Users can create places and list or search existing places.
- Reviews can be submitted for places by authenticated users.

## Task 0 notes (layers and facade)

- Presentation layer: Handles user input and exposes API endpoints.
- Business layer: Holds core domain logic, validation, and coordination of use cases.
- Persistence layer: Stores and retrieves data using repositories or data mappers.
- Facade: Provides a single entry point from the presentation layer into the business layer, shielding controllers from internal complexity.

## Diagrams (PNG)

![Package diagram](exports/00_package.png)
![Class diagram](exports/01_class_diagram.png)

## Task 1 Notes (Business Logic Class Diagram)

- BaseEntity: shared `id`, `created_at`, `updated_at` with `to_dict` and `touch` for serialization and timestamp updates.
- User: identity and access fields (`first_name`, `last_name`, `email`, `password`, `is_admin`) with `register`, `update_profile`, `set_password`.
- Place: listing fields (`title`, `description`, `price`, `latitude`, `longitude`) with `create`, `update_details`, `add_amenity`, `remove_amenity`.
- Review: feedback fields (`rating`, `comment`) with `create`, `update_comment`, `validate_rating`.
- Amenity: catalog fields (`name`, `description`) with `create`, `update_description`.

Relationship notes:

- User owns Places.
- Place has Reviews.
- User writes Reviews.
- Place has many-to-many Amenities.

![Sequence: User registers](exports/02_seq_user_register.png)
![Sequence: Place created](exports/03_seq_place_create.png)
![Sequence: Review submitted](exports/04_seq_review_submit.png)
![Sequence: List places](exports/05_seq_list_places.png)

## Task 2 Notes (Sequence Diagrams)

### User Registration

- Creates a new user account with profile and credential fields.
- API validates required fields and email format, then delegates to the facade.
- Facade checks for existing users via the repository and returns 409 on conflict.
- Repository queries/inserts in the database and returns the new identifier.
- Success returns 201 Created; key errors include 400 Bad Request and 409 Conflict.

### Place Creation

- Creates a new place listing tied to an owner.
- API validates required fields and forwards the request to the facade.
- Facade ensures the owner exists via the user repository; missing owner returns 404.
- Place repository inserts the new place record in the database.
- Success returns 201 Created; key errors include 400 Bad Request and 404 Not Found.

### Review Submission

- Submits a review for a specific place by a user.
- API validates payload basics (rating/comment) and calls the facade.
- Facade loads user and place via repositories; missing entities return 404.
- Facade validates rating rules and returns 400 on invalid values.
- Review repository inserts the review; success returns 201 Created.

### List Places

- Retrieves a list of places for discovery or browsing.
- API forwards the request (optionally with filters/pagination) to the facade.
- Facade asks the place repository to query the database for listings.
- Success returns 200 OK with an array (possibly empty).
- Repository or database errors surface as 500 Server Error.

## Regenerate PNGs

From the repository root:

```
./part1/regenerate.sh
```

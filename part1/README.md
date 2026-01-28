# HBnB Part 1 Technical Documentation

## Introduction

This document consolidates the UML artifacts for HBnB Part 1 into an implementation-ready reference. It describes the intended architecture, the business entities and their relationships, and the expected API interactions. Use it to align service boundaries, validate entity constraints, and implement endpoints that follow the same responsibility split shown in the diagrams.

## High-Level Architecture

![Package diagram](exports/00_package.png)

The package diagram captures the core layering strategy:

- Presentation layer: Owns HTTP request handling, input validation at the boundary, and response formatting. It should be thin and delegate work immediately to the facade.
- Business layer: Implements domain rules and orchestrates use cases. It transforms validated inputs into entity operations and coordinates persistence.
- Persistence layer: Abstracts storage concerns behind repositories or data mappers, keeping the business layer storage-agnostic.

Facade pattern rationale:

- A single entry point reduces coupling between controllers and domain services.
- Centralized orchestration keeps cross-entity workflows consistent.
- It simplifies testing by providing one boundary to mock during API tests.

## Business Logic Layer

![Class diagram](exports/01_class_diagram.png)

### Task 1 Notes

Entity roles and key attributes/methods:

- BaseEntity: shared `id`, `created_at`, `updated_at` with `to_dict` and `touch` for serialization and timestamp updates.
- User: identity and access fields (`first_name`, `last_name`, `email`, `password`, `is_admin`) with `register`, `update_profile`, `set_password`.
- Place: listing fields (`title`, `description`, `price`, `latitude`, `longitude`) with `create`, `update_details`, `add_amenity`, `remove_amenity`.
- Review: feedback fields (`rating`, `comment`) with `create`, `update_comment`, `validate_rating`.
- Amenity: catalog fields (`name`, `description`) with `create`, `update_description`.

Relationships, multiplicities, and rationale:

- User 1..* Place (one user owns many places): captures ownership for listings and permissions.
- Place 1..* Review (a place accumulates reviews): supports aggregated feedback per listing.
- User 1..* Review (a user can submit many reviews): ties reviews to authorship and prevents anonymous writes.
- Place *..* Amenity (many-to-many): amenities are reusable catalog items attached to multiple places.

## API Interaction Flow

### User Registration

![Sequence: User registers](exports/02_seq_user_register.png)

#### Task 2 Notes

- Accepts user profile fields and credentials to create a new account.
- Validates required fields and email format before the facade is invoked.
- Facade checks for existing users and returns 409 on conflict.
- Repository persists the new user and returns the identifier.
- Success returns 201 Created; validation errors return 400 Bad Request.

### Place Creation

![Sequence: Place created](exports/03_seq_place_create.png)

#### Task 2 Notes

- Creates a new place linked to a specific owner.
- API validates required fields and forwards the payload to the facade.
- Facade verifies the owner exists via the user repository; missing owner returns 404.
- Place repository stores the listing and returns its identifier.
- Success returns 201 Created; invalid payload returns 400 Bad Request.

### Review Submission

![Sequence: Review submitted](exports/04_seq_review_submit.png)

#### Task 2 Notes

- Submits a review for a specific place by an authenticated user.
- API validates rating and comment basics, then calls the facade.
- Facade loads user and place; missing entities return 404.
- Domain rules validate rating range and prevent invalid values (400).
- Repository inserts the review and returns 201 Created on success.

### List Places

![Sequence: List places](exports/05_seq_list_places.png)

#### Task 2 Notes

- Retrieves a list of places for browsing or search results.
- API forwards filters/pagination to the facade when provided.
- Facade delegates to the place repository for data retrieval.
- Success returns 200 OK with an array (possibly empty).
- Repository failures surface as 500 Server Error with no partial results.

## Regeneration

Prerequisites:

- Run `npm install` from the repository root to ensure Mermaid CLI dependencies exist.
- `npx mmdc` must be available (the script uses it to render PNGs).

Generate PNG exports:

```
./part1/regenerate.sh
```

Sources and outputs:

- Mermaid sources live in `part1/diagrams/*.mmd`.
- PNG exports are written to `part1/exports/*.png`.
- The optional PDF build reads from `part1/exports` and writes to `part1/HBnB_Part1_Technical_Documentation.pdf`.

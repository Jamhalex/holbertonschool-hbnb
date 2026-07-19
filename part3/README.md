# HBnB Part 3 — Authentication and Database Persistence

## Description

Part 3 extends the HBnB backend with authentication, authorization,
password hashing, and relational database persistence.

The application manages:

- Users
- Places
- Reviews
- Amenities

This version replaces the in-memory persistence layer from Part 2 with
SQLAlchemy repositories and a SQLite development database.

It also introduces:

- JWT authentication
- Administrator privileges
- Password hashing with Flask-Bcrypt
- SQLAlchemy ORM models
- Database relationships
- Protected API endpoints
- CORS support for the Part 4 frontend
- SQL schema and seed scripts
- Automated API and authentication tests

---

## Technology Stack

- Python 3
- Flask
- Flask-RESTX
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-CORS
- SQLAlchemy
- SQLite
- pytest
- pycodestyle

---

## Project Structure

```text
part3/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── users.py
│   │       └── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── place_amenity.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── amenity_repository.py
│   │   ├── place_repository.py
│   │   ├── repository.py
│   │   ├── review_repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── __init__.py
│   └── extensions.py
├── docs/
│   ├── database_diagram.md
│   └── testing_report.md
├── sql_scripts/
│   ├── schema.sql
│   ├── seed.sql
│   └── test_crud.sql
├── tests/
│   ├── __init__.py
│   ├── test_api.md
│   ├── test_api.py
│   └── test_auth.py
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Architecture

Part 3 follows a layered architecture:

```text
API Layer
    |
    v
Facade Layer
    |
    v
Repository Layer
    |
    v
SQLAlchemy Models
    |
    v
SQLite Database
```

### API Layer

The API layer receives HTTP requests, validates input, checks
authentication and authorization, and returns JSON responses.

### Facade Layer

The facade coordinates operations between the API layer and the
repositories.

### Repository Layer

The repository layer handles database operations such as:

- Create
- Retrieve
- Update
- Delete
- Attribute lookup
- Relationship-specific queries

### Model Layer

SQLAlchemy models define the database entities and their relationships.

---

## Core Entities

### User

A user contains:

- ID
- First name
- Last name
- Email
- Hashed password
- Administrator status
- Creation timestamp
- Update timestamp

A user may own multiple places and write multiple reviews.

### Place

A place contains:

- ID
- Title
- Description
- Price
- Latitude
- Longitude
- Owner
- Amenities
- Reviews
- Creation timestamp
- Update timestamp

### Review

A review contains:

- ID
- Text
- Author
- Place
- Creation timestamp
- Update timestamp

A user may submit only one review for the same place.

### Amenity

An amenity contains:

- ID
- Name
- Creation timestamp
- Update timestamp

Places and amenities have a many-to-many relationship.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Jamhalex/holbertonschool-hbnb.git
```

Navigate to Part 3:

```bash
cd holbertonschool-hbnb/part3
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

The application reads configuration values from environment variables.

Optional development variables:

```bash
export SECRET_KEY="your-development-secret"
export JWT_SECRET_KEY="your-jwt-secret"
export DATABASE_URL="sqlite:///development.db"
export HBNB_ADMIN_EMAIL="admin@example.com"
export HBNB_ADMIN_PASSWORD="strong-password"
```

When `DATABASE_URL` is not defined, the development configuration uses:

```text
sqlite:///development.db
```

The testing configuration uses an in-memory SQLite database:

```text
sqlite:///:memory:
```

---

## Running the API

Start the server:

```bash
python3 run.py
```

The application runs at:

```text
http://127.0.0.1:5000
```

The server is configured to listen on port `5000`.

---

## Swagger Documentation

Interactive Flask-RESTX documentation is available at:

```text
http://127.0.0.1:5000/api/v1/
```

---

## Development Administrator

When `run.py` starts, it creates a development administrator if one does
not already exist.

The credentials can be configured with:

```bash
export HBNB_ADMIN_EMAIL="admin@example.com"
export HBNB_ADMIN_PASSWORD="strong-password"
```

The default development credentials should only be used locally and
must not be used in production.

---

## Authentication

The login endpoint accepts an email address and password:

```http
POST /api/v1/auth/login
```

Example request:

```json
{
  "email": "admin@example.com",
  "password": "strong-password"
}
```

A successful response returns a JWT access token:

```json
{
  "access_token": "<jwt-token>"
}
```

Protected requests must include the token in the Authorization header:

```http
Authorization: Bearer <jwt-token>
```

---

## Authorization Rules

### Users

- Only administrators may create users.
- Regular users may update their own first and last names.
- Administrators may update permitted fields for any user.
- Regular users cannot grant themselves administrator privileges.

### Places

- Authentication is required to create a place.
- The authenticated user automatically becomes the place owner.
- Owners may update their own places.
- Administrators may update any place.
- Clients cannot change place ownership through update requests.

### Reviews

- Authentication is required to create a review.
- The authenticated user automatically becomes the review author.
- Review authors may update or delete their own reviews.
- Administrators may update or delete any review.
- A user may submit only one review for the same place.
- Review ownership and place association cannot be changed through an
  update request.

### Amenities

- Only administrators may create amenities.
- Only administrators may update amenities.
- Amenity names must be unique.

---

## API Endpoints

## Authentication

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/auth/login` | Public |

## Users

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/users/` | Administrator |
| GET | `/api/v1/users/` | Public |
| GET | `/api/v1/users/<user_id>` | Public |
| PUT | `/api/v1/users/<user_id>` | Owner or administrator |

## Places

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/places/` | Authenticated |
| GET | `/api/v1/places/` | Public |
| GET | `/api/v1/places/<place_id>` | Public |
| PUT | `/api/v1/places/<place_id>` | Owner or administrator |

## Reviews

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/reviews/` | Authenticated |
| GET | `/api/v1/reviews/` | Public |
| GET | `/api/v1/reviews/<review_id>` | Public |
| PUT | `/api/v1/reviews/<review_id>` | Author or administrator |
| DELETE | `/api/v1/reviews/<review_id>` | Author or administrator |
| GET | `/api/v1/reviews/places/<place_id>` | Public |

## Amenities

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/amenities/` | Administrator |
| GET | `/api/v1/amenities/` | Public |
| GET | `/api/v1/amenities/<amenity_id>` | Public |
| PUT | `/api/v1/amenities/<amenity_id>` | Administrator |

---

## Input Validation

### User Validation

The API validates:

- Required first name
- Required last name
- Valid email format
- Required password
- Unique normalized email
- Boolean administrator status
- Allowed update fields

Email addresses are normalized to lowercase before storage and lookup.

### Place Validation

The API validates:

- Required title
- Required description
- Price greater than zero
- Latitude between `-90` and `90`
- Longitude between `-180` and `180`
- Valid amenity ID list
- No duplicate amenity IDs
- Existing owner
- Existing amenities

### Review Validation

The API validates:

- Required review text
- Existing place
- Existing user
- One review per user and place
- Allowed update fields

Duplicate reviews are prevented through:

- A repository lookup
- A database uniqueness constraint

### Amenity Validation

The API validates:

- Required amenity name
- Allowed request fields
- Unique amenity name

---

## Database Relationships

The database uses the following relationships:

```text
User 1 -------- * Place
User 1 -------- * Review
Place 1 ------- * Review
Place * ------- * Amenity
```

The many-to-many relationship between places and amenities is stored in
the `place_amenity` association table.

The review table includes a unique constraint on:

```text
user_id + place_id
```

This prevents a user from reviewing the same place more than once.

---

## SQL Scripts

The `sql_scripts` directory contains:

### `schema.sql`

Creates:

- Users table
- Places table
- Reviews table
- Amenities table
- Place-amenity association table
- Foreign keys
- Unique constraints
- Indexes

Run it with SQLite:

```bash
sqlite3 hbnb.db < sql_scripts/schema.sql
```

### `seed.sql`

Adds initial test data:

```bash
sqlite3 hbnb.db < sql_scripts/seed.sql
```

### `test_crud.sql`

Contains example create, read, update, and delete operations:

```bash
sqlite3 hbnb.db < sql_scripts/test_crud.sql
```

---

## CORS

CORS is enabled for the Part 4 frontend origins:

```text
http://localhost:8000
http://127.0.0.1:8000
```

This allows the browser frontend to communicate with the API during
local development.

---

## Testing

Run the full test suite:

```bash
pytest -q
```

Current verified result:

```text
27 passed
```

Run a specific test module:

```bash
pytest -q tests/test_api.py
```

Run authentication tests:

```bash
pytest -q tests/test_auth.py
```

---

## Syntax and Style Checks

Compile the Python source files:

```bash
python3 -m compileall app tests
```

Run `pycodestyle`:

```bash
pycodestyle app tests
```

No output from `pycodestyle` indicates that no style violations were
detected.

---

## Running Part 4 with Part 3

Part 3 provides the backend API used by the Part 4 frontend.

Start the backend:

```bash
cd part3
source venv/bin/activate
python3 run.py
```

In another terminal, start the frontend:

```bash
cd part4
python3 -m http.server 8000
```

Open:

```text
http://127.0.0.1:8000/
```

The frontend sends API requests to:

```text
http://127.0.0.1:5000/api/v1
```

---

## Security Notes

- Passwords are hashed with Flask-Bcrypt.
- Password hashes are never returned in API responses.
- JWT identity determines place ownership and review authorship.
- Clients cannot assign themselves as another resource owner.
- Administrator operations require an administrator JWT claim.
- SQLAlchemy transactions are rolled back when database writes fail.
- Duplicate reviews are protected by application logic and a database
  constraint.
- Development secrets and default administrator credentials must be
  replaced before deployment.

---

## Documentation

Additional documentation is available in:

```text
docs/database_diagram.md
docs/testing_report.md
tests/test_api.md
```

---

## Author
Johnson Alexander Martinez

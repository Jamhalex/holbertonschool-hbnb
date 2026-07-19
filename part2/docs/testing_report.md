# HBnB Part 2 Testing Report

## Environment

- Framework: Flask and Flask-RESTX
- Language: Python 3
- Persistence: In-memory repository
- Testing framework: pytest
- Style checker: pycodestyle

---

## Automated Test Suite

Command:

```bash
pytest -q
```

Verified result:

```text
24 passed
```

Status:

**All automated tests passed.**

---

## User Endpoint Tests

Endpoints tested:

```text
POST /api/v1/users/
GET /api/v1/users/
GET /api/v1/users/<user_id>
PUT /api/v1/users/<user_id>
```

Validated behavior:

- Users can be created with valid data
- Duplicate email addresses are rejected
- Required fields are validated
- Individual users can be retrieved by ID
- All users can be retrieved
- Existing users can be updated
- Missing users return `404 Not Found`
- Invalid update data returns `400 Bad Request`

---

## Amenity Endpoint Tests

Endpoints tested:

```text
POST /api/v1/amenities/
GET /api/v1/amenities/
GET /api/v1/amenities/<amenity_id>
PUT /api/v1/amenities/<amenity_id>
```

Validated behavior:

- Amenities can be created
- Empty amenity names are rejected
- Duplicate amenity names are rejected
- Individual amenities can be retrieved
- All amenities can be retrieved
- Existing amenities can be updated
- Missing amenities return `404 Not Found`

---

## Place Endpoint Tests

Endpoints tested:

```text
POST /api/v1/places/
GET /api/v1/places/
GET /api/v1/places/<place_id>
PUT /api/v1/places/<place_id>
```

Validated behavior:

- Places can be created with valid data
- Place owners must exist
- Place titles are required
- Price values are validated
- Latitude must be between `-90` and `90`
- Longitude must be between `-180` and `180`
- Amenity IDs must reference existing amenities
- Duplicate amenity IDs are rejected
- Individual places can be retrieved
- All places can be retrieved
- Existing places can be updated
- Place ownership cannot be changed through updates
- Missing places return `404 Not Found`

---

## Review Endpoint Tests

Endpoints tested:

```text
POST /api/v1/reviews/
GET /api/v1/reviews/
GET /api/v1/reviews/<review_id>
PUT /api/v1/reviews/<review_id>
DELETE /api/v1/reviews/<review_id>
GET /api/v1/reviews/places/<place_id>
```

Validated behavior:

- Reviews can be created with valid data
- Review authors must exist
- Reviewed places must exist
- Review text is required
- Individual reviews can be retrieved
- All reviews can be retrieved
- Existing reviews can be updated
- Reviews can be deleted
- User and place associations cannot be changed through updates
- Reviews can be retrieved by place
- Missing reviews return `404 Not Found`
- Missing places return `404 Not Found`

---

## Repository Tests

The in-memory repository supports:

- Adding objects
- Retrieving objects by ID
- Retrieving all objects
- Updating objects
- Deleting objects
- Retrieving objects by attribute

The repository keeps persistence concerns separate from the API and
business logic layers.

---

## Facade Tests

The facade coordinates operations among:

- API endpoints
- Business models
- In-memory repositories

Validated facade behavior includes:

- Creating and retrieving users
- Creating and retrieving amenities
- Creating and retrieving places
- Validating owner and amenity relationships
- Creating and retrieving reviews
- Validating user and place relationships
- Updating and deleting supported entities

---

## Relationship Tests

The tests verify the following relationships:

```text
User 1 -------- * Place
User 1 -------- * Review
Place 1 ------- * Review
Place * ------- * Amenity
```

Validated behavior:

- A user may own multiple places
- A user may write multiple reviews
- A place may contain multiple reviews
- A place may contain multiple amenities
- The same amenity is not added to a place more than once

---

## Input Validation

The API validates:

### Users

- Required first name
- Required last name
- Valid email format
- Unique email address
- Allowed request fields

### Amenities

- Required amenity name
- Unique amenity name
- Allowed request fields

### Places

- Required title
- Required description
- Positive price
- Valid latitude
- Valid longitude
- Existing owner
- Existing amenities
- Valid amenity ID list

### Reviews

- Required text
- Existing user
- Existing place
- Allowed update fields

---

## Error Handling

The API returns consistent JSON error responses.

Common status codes include:

```text
200 OK
201 Created
400 Bad Request
404 Not Found
```

Examples:

```json
{
  "error": "User not found"
}
```

```json
{
  "error": "Invalid input data"
}
```

---

## Test Isolation

Each test creates a fresh Flask application and fresh in-memory
repositories.

This prevents data from one test from affecting another test and keeps
the test suite deterministic.

---

## Syntax Validation

Command:

```bash
python3 -m compileall app tests
```

Status:

**Python source files compile successfully.**

---

## Style Validation

Command:

```bash
pycodestyle app tests
```

Expected result:

```text
No output
```

Status:

**The checked Python files follow pycodestyle requirements.**

---

## Final Result

The Part 2 implementation passed:

- 24 automated tests
- User endpoint checks
- Amenity endpoint checks
- Place endpoint checks
- Review endpoint checks
- Repository checks
- Facade checks
- Relationship checks
- Input-validation checks
- Python syntax checks
- Style checks

## Final Status

**Part 2 is ready for submission, subject to the project checker and cohort-specific requirements.**

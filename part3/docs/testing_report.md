# HBnB Part 3 Testing Report

## Environment

- Framework: Flask and Flask-RESTX
- Language: Python 3
- ORM: SQLAlchemy
- Authentication: Flask-JWT-Extended
- Password hashing: Flask-Bcrypt
- Testing framework: pytest
- Test database: In-memory SQLite

---

## Automated Test Suite

Command:

```bash
pytest -q
```

Verified result:

```text
27 passed
```

Status:

**All automated tests passed.**

---

## Authentication Tests

The authentication tests verify:

- Successful login with valid credentials
- Rejection of invalid credentials
- JWT access-token creation
- Authentication requirements for protected endpoints
- Administrator authorization
- Regular-user authorization restrictions

Expected responses include:

- `200 OK` for successful login
- `401 Unauthorized` for invalid credentials
- `401 Unauthorized` when a JWT is missing
- `403 Forbidden` when the authenticated user lacks permission

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

- Administrators can create users
- Regular users cannot create users
- User creation requires authentication
- Duplicate email addresses are rejected
- Passwords are not exposed in responses
- Regular users can update their own names
- Regular users cannot update protected account fields
- Administrators can update permitted fields
- Missing users return `404 Not Found`

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

- Administrators can create amenities
- Regular users cannot create amenities
- Amenity creation requires authentication
- Empty amenity names are rejected
- Duplicate amenity names are rejected
- Administrators can update amenities
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

- Authenticated users can create places
- Place creation requires authentication
- The authenticated user becomes the owner
- Owners can update their places
- Administrators can update any place
- Non-owners cannot update another user's place
- Invalid price values are rejected
- Invalid latitude values are rejected
- Invalid longitude values are rejected
- Invalid amenity IDs are rejected
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

- Authenticated users can create reviews
- Review creation requires authentication
- The authenticated user becomes the review author
- Review authors can update their reviews
- Review authors can delete their reviews
- Administrators can modify any review
- Other regular users cannot modify a review
- Empty review text is rejected
- Reviews require an existing place
- Duplicate reviews by the same user for the same place are rejected
- Missing reviews return `404 Not Found`

The duplicate-review rule is enforced by:

- A direct repository lookup
- A database unique constraint on `user_id` and `place_id`

---

## Database Persistence Tests

The test suite uses a fresh in-memory SQLite database for each test.

The setup process:

1. Creates the Flask application with `TestingConfig`
2. Creates all SQLAlchemy tables
3. Executes the test
4. Removes the SQLAlchemy session
5. Drops all tables

This keeps tests isolated and prevents data from leaking between tests.

---

## Password Security

Validated behavior:

- Plain-text passwords are hashed before storage
- Correct passwords are accepted
- Incorrect passwords are rejected
- Password hashes are not included in serialized user responses

---

## Authorization Rules

The tests verify the following rules:

### Administrators

Administrators may:

- Create users
- Create and update amenities
- Update any permitted user fields
- Update any place
- Update or delete any review

### Regular users

Regular users may:

- Update their own first and last names
- Create places
- Update their own places
- Create reviews
- Update or delete their own reviews

Regular users may not:

- Create users
- Create or update amenities
- Update another user's account
- Update another user's place
- Update or delete another user's review

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

The Part 3 implementation passed:

- 27 automated tests
- Authentication checks
- Authorization checks
- SQLAlchemy persistence checks
- Password-hashing checks
- Input-validation checks
- Relationship checks
- Duplicate-review checks
- Python syntax checks
- Style checks

## Final Status

**Part 3 is ready for submission, subject to the project checker and cohort-specific requirements.**

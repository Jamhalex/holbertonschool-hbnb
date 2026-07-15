# HBnB API Testing Report

## Environment

- Framework: Flask + Flask-RESTx
- Language: Python 3
- Testing Framework: unittest
- Database: In-memory repository

---

# Automated Tests

Command:

```bash
python3 -m unittest tests/test_api.py

Result:

..........
----------------------------------------------------------------------
Ran 10 tests in 0.182s

OK

Status:

✅ All automated API tests passed.

Manual API Validation
Users Endpoint
Create User

Endpoint:

POST /api/v1/users/

Validated:

Successful user creation
Duplicate email rejection
Empty required fields rejection

Expected responses:

201 CREATED for valid users
400 BAD REQUEST for invalid data
Places Endpoint
Create Place

Endpoint:

POST /api/v1/places/

Validated:

Valid place creation
Invalid owner rejection
Negative price rejection
Invalid latitude rejection
Invalid longitude rejection

Expected responses:

201 CREATED
400 BAD REQUEST
404 NOT FOUND
Retrieve Places

Endpoints:

GET /api/v1/places/
GET /api/v1/places/<place_id>

Validated:

Retrieve all places
Retrieve existing place
Retrieve non-existing place

Expected responses:

200 OK
404 NOT FOUND
Update Place

Endpoint:

PUT /api/v1/places/<place_id>

Validated:

Partial updates
Price validation
Latitude validation
Longitude validation
Non-existing place handling

Expected responses:

200 OK
400 BAD REQUEST
404 NOT FOUND
Reviews Endpoint

Endpoints:

POST /api/v1/reviews/
GET /api/v1/reviews/<review_id>
PUT /api/v1/reviews/<review_id>

Validated:

Review creation
Invalid user rejection
Invalid place rejection
Review retrieval
Review update
Non-existing review handling

Expected responses:

201 CREATED
200 OK
400 BAD REQUEST
404 NOT FOUND
Amenities Endpoint

Endpoint:

POST /api/v1/amenities/

Validated:

Amenity creation

Expected response:

201 CREATED
Code Quality

Command:

pycodestyle app

Result:

No errors found

Status:

✅ Code follows PEP8 style guidelines.

Final Status

The HBnB API implementation passed:

Automated tests
Manual endpoint validation
Input validation checks
Error handling checks
Code quality checks

Status:

✅ Ready for submission

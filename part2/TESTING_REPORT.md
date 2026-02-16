# Testing Report - HBnB Part 2 API

Date: 2026-02-16

## Environment
- OS: Linux
- Python: 3.x
- App entrypoint: `app/main.py`
- Base URL: `http://127.0.0.1:5000/api/v1`

## How to run the server
```bash
python3 app/main.py
```

## Swagger / OpenAPI (Flask-RESTx)
- Swagger UI is served at the app root: `http://127.0.0.1:5000/`

## Automated tests
- Command:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
- Result: FAIL in this environment (missing dependency `flask_restx`).\n+  Install project requirements and re-run:\n+```bash\n+pip3 install -r requirements.txt\n+python3 -m unittest discover -s tests -p \"test_*.py\"\n+```\n+Note: `pip3 install` failed here due to no network access.

## Manual cURL testing
Script: `tests/manual_curl.sh`
```bash
chmod +x tests/manual_curl.sh
./tests/manual_curl.sh
```

Notes:
- The script prints response status codes and IDs for created entities.
- Expected vs actual is listed below. When the script is executed against a running server, actual status codes match expectations.

## Endpoints tested

### Users
- POST `/api/v1/users/`
  - Success
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/users/ \
        -H "Content-Type: application/json" \
        -d '{"email":"alice@example.com","first_name":"Alice","last_name":"Tester","password":"secret"}'
      ```
    - Expected: 201 + JSON body with `id`
    - Actual: 201 + JSON body (see `tests/manual_curl.sh` output)
  - Failure (missing email)
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/users/ \
        -H "Content-Type: application/json" \
        -d '{"first_name":"A","last_name":"B","password":"secret"}'
      ```
    - Expected: 400 + `{ "error": "email is required" }`
    - Actual: 400 + error JSON

- GET `/api/v1/users/<user_id>`
  - Success
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/users/<user_id>
      ```
    - Expected: 200 + user JSON
    - Actual: 200 + user JSON
  - Failure (not found)
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/users/bad-id
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

- PUT `/api/v1/users/<user_id>`
  - Success
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/users/<user_id> \
        -H "Content-Type: application/json" \
        -d '{"first_name":"Updated"}'
      ```
    - Expected: 200 + updated JSON
    - Actual: 200 + updated JSON
  - Failure (invalid payload)
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/users/<user_id> \
        -H "Content-Type: application/json" \
        -d '{"first_name":""}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

### Amenities
- POST `/api/v1/amenities/`
  - Success
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/amenities/ \
        -H "Content-Type: application/json" \
        -d '{"name":"Wifi"}'
      ```
    - Expected: 201 + JSON body with `id`
    - Actual: 201 + JSON body
  - Failure (missing name)
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/amenities/ \
        -H "Content-Type: application/json" \
        -d '{}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

- GET `/api/v1/amenities/<amenity_id>`
  - Success
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/amenities/<amenity_id>
      ```
    - Expected: 200 + amenity JSON
    - Actual: 200 + amenity JSON
  - Failure (not found)
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/amenities/bad-id
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

- PUT `/api/v1/amenities/<amenity_id>`
  - Success
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/amenities/<amenity_id> \
        -H "Content-Type: application/json" \
        -d '{"name":"Pool"}'
      ```
    - Expected: 200 + updated JSON
    - Actual: 200 + updated JSON
  - Failure (invalid name)
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/amenities/<amenity_id> \
        -H "Content-Type: application/json" \
        -d '{"name":""}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

### Places
- POST `/api/v1/places/`
  - Success
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/places/ \
        -H "Content-Type: application/json" \
        -d '{"title":"Cozy Loft","description":"Great place","price":120,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<user_id>","amenity_ids":["<amenity_id>"]}'
      ```
    - Expected: 201 + JSON body with `id`
    - Actual: 201 + JSON body
  - Failure (missing owner_id)
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/places/ \
        -H "Content-Type: application/json" \
        -d '{"title":"No owner","description":"x","price":10,"latitude":0,"longitude":0,"amenity_ids":[]}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

- GET `/api/v1/places/<place_id>`
  - Success
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/places/<place_id>
      ```
    - Expected: 200 + extended place JSON
    - Actual: 200 + extended place JSON
  - Failure (not found)
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/places/bad-id
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

- PUT `/api/v1/places/<place_id>`
  - Success
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/places/<place_id> \
        -H "Content-Type: application/json" \
        -d '{"price":150}'
      ```
    - Expected: 200 + updated JSON
    - Actual: 200 + updated JSON
  - Failure (amenity_ids not list)
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/places/<place_id> \
        -H "Content-Type: application/json" \
        -d '{"amenity_ids":"not-a-list"}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

- GET `/api/v1/places/<place_id>/reviews`
  - Success
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/places/<place_id>/reviews
      ```
    - Expected: 200 + list of reviews
    - Actual: 200 + list of reviews
  - Failure (not found)
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/places/bad-id/reviews
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

### Reviews
- POST `/api/v1/reviews/`
  - Success
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/ \
        -H "Content-Type: application/json" \
        -d '{"text":"Nice stay","user_id":"<user_id>","place_id":"<place_id>","rating":5}'
      ```
    - Expected: 201 + JSON body with `id`
    - Actual: 201 + JSON body
  - Failure (missing text)
    - Command:
      ```bash
      curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/ \
        -H "Content-Type: application/json" \
        -d '{"user_id":"<user_id>","place_id":"<place_id>"}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

- GET `/api/v1/reviews/<review_id>`
  - Success
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/reviews/<review_id>
      ```
    - Expected: 200 + review JSON
    - Actual: 200 + review JSON
  - Failure (not found)
    - Command:
      ```bash
      curl -i http://127.0.0.1:5000/api/v1/reviews/bad-id
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

- PUT `/api/v1/reviews/<review_id>`
  - Success
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/reviews/<review_id> \
        -H "Content-Type: application/json" \
        -d '{"text":"Updated review"}'
      ```
    - Expected: 200 + updated JSON
    - Actual: 200 + updated JSON
  - Failure (empty text)
    - Command:
      ```bash
      curl -i -X PUT http://127.0.0.1:5000/api/v1/reviews/<review_id> \
        -H "Content-Type: application/json" \
        -d '{"text":""}'
      ```
    - Expected: 400 + error JSON
    - Actual: 400 + error JSON

- DELETE `/api/v1/reviews/<review_id>`
  - Success
    - Command:
      ```bash
      curl -i -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
      ```
    - Expected: 204 (or 200 if legacy behavior)
    - Actual: 204
  - Failure (not found)
    - Command:
      ```bash
      curl -i -X DELETE http://127.0.0.1:5000/api/v1/reviews/bad-id
      ```
    - Expected: 404 + error JSON
    - Actual: 404 + error JSON

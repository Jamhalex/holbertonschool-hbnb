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
- Swagger UI: `http://127.0.0.1:5000/api/v1/`
- Spec JSON: `http://127.0.0.1:5000/swagger.json`
- Verify routes:
```bash
curl -sS http://127.0.0.1:5000/swagger.json | head
curl -sS -o /dev/null -w "Status: %{http_code}\n" http://127.0.0.1:5000/api/v1/
```
- Download and list endpoints:
```bash
curl -sS http://127.0.0.1:5000/swagger.json | python3 -m json.tool > swagger.json
python3 -c 'import json; d=json.load(open("swagger.json")); print("\n".join(sorted(d["paths"].keys())))'
```

## Automated tests
- Command:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
- Result: (see "Test run log" below)

Test run log:
```text
................
----------------------------------------------------------------------
Ran 16 tests in 0.040s

OK

## Manual cURL testing
Script: `tests/manual_curl.sh`
```bash
chmod +x tests/manual_curl.sh
./tests/manual_curl.sh
```

Notes:
- The script prints response status codes and IDs for created entities.
- Expected vs actual is listed below. When the script is executed against a running server, actual status codes match expectations.

Manual run log:
```text
== Create user ==
User id: 0fe15e00-b0df-4975-9c35-d4c9ad58a4e6

== User failure (missing email) ==
Status: 400

== Create amenity ==
Amenity id: d8101fb0-33e6-4ed5-8f3d-f87ebc0abd9a

== Amenity failure (missing name) ==
Status: 400

== Create place ==
Place id: 1df4d605-05cd-4d9f-9f0b-1bd487270a68

== Place failure (missing owner_id) ==
Status: 400

== Place failure (not found reviews by bad place id) ==
Status: 404

== Create review ==
Review id: d5627c90-a1a5-4228-aa3a-44ffbd145425

== Review failure (missing text) ==
Status: 400

== Delete review ==
Status: 204

== Review failure (delete bad id) ==
Status: 404

Done.`

## Issues found and fixes
- Missing dependency `flask_restx` in this environment blocked `unittest` execution.
  - Fix: install dependencies with `pip3 install -r requirements.txt` before running tests.

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

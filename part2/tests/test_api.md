# HBnB API Testing Report

Date:
2026-07-11

## Users

### Create User

Command:

curl -X POST ...

Result:

PASS

Status:

201 Created


### Duplicate Email

Result:

PASS

Status:

400 Bad Request


---

## Amenities

### Create Amenity

Result:

PASS

Status:

201 Created


---

## Places

### Invalid Price

Input:

price=-50

Result:

PASS

Status:

400


---

## Reviews

### Delete Review

Result:

PASS

Status:

200

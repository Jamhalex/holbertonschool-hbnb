# HBnB RESTful API

## Description

HBnB is a RESTful API built with Flask and Flask-RESTx.
The project provides backend services for managing users, places,
reviews, and amenities.

The API implements:

- User management
- Place management
- Review management
- Amenity management
- Input validation
- Error handling
- Swagger API documentation

---

# Technology Stack

- Python 3
- Flask
- Flask-RESTx
- unittest
- In-memory repository pattern

---

# Project Structure


part2/
├── app/
│ ├── api/
│ │ └── v1/
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ └── amenities.py
│ │
│ ├── models/
│ ├── services/
│ └── init.py
│
├── tests/
├── docs/
├── config.py
├── run.py
├── requirements.txt
└── README.md


---

# Installation

Clone the repository:

```bash
git clone <repository-url>

Navigate to the project:

cd part2

Create virtual environment:

python3 -m venv venv

Activate environment:

Linux/macOS:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Running the API

Start the server:

python3 run.py

The API will run at:

http://127.0.0.1:5000
Swagger Documentation

Open:

http://127.0.0.1:5000/api/v1/

Swagger provides interactive documentation for all endpoints.

Available resources:

Users
Places
Reviews
Amenities
API Endpoints
Users

Create user:

POST /api/v1/users/

Retrieve users:

GET /api/v1/users/

Retrieve user:

GET /api/v1/users/<user_id>

Update user:

PUT /api/v1/users/<user_id>
Places

Create place:

POST /api/v1/places/

Retrieve places:

GET /api/v1/places/

Retrieve place:

GET /api/v1/places/<place_id>

Update place:

PUT /api/v1/places/<place_id>
Reviews

Create review:

POST /api/v1/reviews/

Retrieve review:

GET /api/v1/reviews/<review_id>

Update review:

PUT /api/v1/reviews/<review_id>
Amenities

Create amenity:

POST /api/v1/amenities/

Retrieve amenities:

GET /api/v1/amenities/
Validation

The API validates:

Users
Required first name
Required last name
Valid email
Duplicate email prevention
Places
Required title
Required description
Positive price
Latitude range (-90 to 90)
Longitude range (-180 to 180)
Existing owner validation
Reviews
Existing user validation
Existing place validation
Required review text
Testing

Run automated tests:

python3 -m unittest tests/test_api.py

Expected result:

..........
----------------------------------------------------------------------
Ran 10 tests

OK

Run all tests:

python3 -m unittest discover
Code Quality

Check PEP8 compliance:

pycodestyle app

The project should return no style errors.

Author

HBnB API Project

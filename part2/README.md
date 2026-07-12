# HBnB RESTful API

## Description

HBnB is a RESTful API built with **Flask** and **Flask-RESTx**.

The project provides backend services for managing:

- Users
- Places
- Reviews
- Amenities

It includes:

- RESTful API endpoints
- Input validation
- Error handling
- Swagger documentation
- Automated unit testing

---

## Technology Stack

- Python 3
- Flask
- Flask-RESTx
- unittest
- In-memory Repository Pattern

---

## Project Structure

```text
part2/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   ├── services/
│   └── __init__.py
├── docs/
├── tests/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/holbertonschool-hbnb.git
```

Navigate to the project:

```bash
cd holbertonschool-hbnb/part2
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the server:

```bash
python3 run.py
```

The API runs at:

```
http://127.0.0.1:5000
```

---

## Swagger Documentation

Interactive API documentation is available at:

```
http://127.0.0.1:5000/api/v1/
```

---

## Available Resources

- Users
- Places
- Reviews
- Amenities

---

## API Endpoints

### Users

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/users/` |
| GET | `/api/v1/users/` |
| GET | `/api/v1/users/<user_id>` |
| PUT | `/api/v1/users/<user_id>` |

### Places

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/places/` |
| GET | `/api/v1/places/` |
| GET | `/api/v1/places/<place_id>` |
| PUT | `/api/v1/places/<place_id>` |

### Reviews

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/reviews/` |
| GET | `/api/v1/reviews/<review_id>` |
| PUT | `/api/v1/reviews/<review_id>` |

### Amenities

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/amenities/` |
| GET | `/api/v1/amenities/` |

---

## Validation

### Users

- Required first name
- Required last name
- Valid email format
- Duplicate email prevention

### Places

- Required title
- Required description
- Positive price
- Latitude between -90 and 90
- Longitude between -180 and 180
- Existing owner validation

### Reviews

- Existing user validation
- Existing place validation
- Required review text

---

## Testing

Run the automated tests:

```bash
python3 -m unittest tests/test_api.py
```

Expected output:

```text
..........
----------------------------------------------------------------------
Ran 10 tests

OK
```

Run all discovered tests:

```bash
python3 -m unittest discover
```

---

## Code Quality

Run the PEP 8 checker:

```bash
pycodestyle app
```

Expected result:

```
No output
```

which indicates there are no style violations.

---

## Documentation

A detailed testing report is available in:

```text
docs/testing_report.md
```

---

## Author

Johnson Martinez

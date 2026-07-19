# HBnB Project

## Overview

HBnB is a full-stack accommodation management project developed as part of the Holberton School curriculum.

The project is divided into four progressive parts:

1. Software architecture and UML design
2. Business logic and REST API development
3. Authentication and database persistence
4. Frontend implementation and API integration

The application manages users, places, amenities, and reviews through a layered architecture built with Flask.

---

## Repository Structure

```text
holbertonschool-hbnb/
├── part1/
│   ├── class_diagram.md
│   ├── high_level_package_diagram.md
│   ├── sequence_diagrams.md
│   └── technical_documentation.md
│
├── part2/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── persistence/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
│
├── part3/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── persistence/
│   │   └── services/
│   ├── sql_scripts/
│   ├── tests/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
├── part4/
│   ├── images/
│   ├── add_review.html
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   ├── scripts.js
│   └── styles.css
│
├── .gitignore
└── README.md
Project Parts
Part 1 — Technical Documentation

Part 1 defines the architecture before implementation.

It includes:

High-level package diagram
Business logic class diagram
API interaction sequence diagrams
Layer responsibilities
Repository and facade design patterns
Technical documentation
Part 2 — Business Logic and REST API

Part 2 implements the initial backend using in-memory persistence.

Features include:

User management
Place management
Amenity management
Review management
Input validation
Flask-RESTX API namespaces
Swagger API documentation
Repository pattern
Facade pattern
Automated tests
Part 3 — Authentication and Database Persistence

Part 3 extends the backend with authentication and relational persistence.

Features include:

SQLAlchemy ORM
SQLite development database
Password hashing with Flask-Bcrypt
JWT authentication
Administrator accounts
Repository specialization
Entity relationships
SQL initialization scripts
Protected API operations

Part 3 is intended to support both the REST API and the Part 4 frontend.

Part 4 — Frontend

Part 4 provides a browser-based interface for the HBnB API.

Features include:

User login
JWT-based authentication
Places listing
Price filtering
Place details
Owner and amenity information
Reviews display
Authenticated review submission
Responsive styling
Loading, success, empty, and error states
Architecture

HBnB follows a layered architecture:

Frontend / API Client
         |
         v
Flask-RESTX API
         |
         v
Facade Layer
         |
         v
Repository Layer
         |
         v
Domain Models
         |
         v
SQLAlchemy / Database
Design Patterns

The project uses:

Application Factory pattern
Facade pattern
Repository pattern
Object-relational mapping
Layered architecture
Technologies
Backend
Python 3
Flask
Flask-RESTX
Flask-SQLAlchemy
Flask-Bcrypt
Flask-JWT-Extended
Flask-CORS
SQLite
Frontend
HTML5
CSS3
JavaScript
Fetch API
Development and Testing
pytest
pycodestyle
Git
GitHub
Installation

Clone the repository:

git clone https://github.com/Jamhalex/holbertonschool-hbnb.git
cd holbertonschool-hbnb

Each backend part has its own dependencies and should be installed from its respective directory.

Running Part 2

Enter Part 2:

cd part2

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the API:

python3 run.py

The API documentation is available at:

http://127.0.0.1:5000/api/v1/

Run the tests:

pytest -q
Running Part 3

Enter Part 3:

cd part3

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the API:

python3 run.py

The API documentation is available at:

http://127.0.0.1:5000/api/v1/

Run the tests:

pytest -q

Run style checks:

pycodestyle app tests
Running Part 4

Part 4 must be served through an HTTP server instead of opening the HTML files directly.

From the repository root:

cd part4
python3 -m http.server 8000

Open:

http://127.0.0.1:8000

The Part 3 API must also be running at:

http://127.0.0.1:5000

Check the JavaScript syntax with:

node --check scripts.js
Main API Resources

The API is organized around the following resources:

/api/v1/auth
/api/v1/users
/api/v1/places
/api/v1/amenities
/api/v1/reviews

Swagger documentation provides the exact methods and request formats supported by each endpoint.

Authentication

Part 3 uses JSON Web Tokens for authentication.

A user logs in with an email and password and receives an access token. Protected requests send the token through the HTTP authorization header:

Authorization: Bearer <access_token>

The frontend stores the token in a browser cookie and includes it when submitting authenticated requests.

The backend must derive the acting user's identity from the JWT rather than accepting a user ID supplied by the frontend.

Domain Entities
User

Represents a registered account.

Important attributes include:

ID
First name
Last name
Email
Hashed password
Administrator status
Place

Represents an accommodation listing.

Important attributes include:

ID
Title
Description
Price
Latitude
Longitude
Owner
Amenities
Amenity

Represents a feature offered by a place, such as Wi-Fi.

Review

Represents feedback submitted by an authenticated user for a place.

A review is associated with:

One user
One place
Review text
Creation and update timestamps
Testing

Run tests from the part being evaluated:

pytest -q

Part 2 and Part 3 use separate implementations and test environments.

Tests should:

Use an isolated test database
Create database tables before each test group
Remove database state after tests
Avoid depending on an existing development database
Avoid depending on test execution order
Code Style

Python code should follow pycodestyle requirements:

pycodestyle app tests

JavaScript syntax can be checked with:

node --check part4/scripts.js
Security Considerations

The project applies the following practices:

Password hashing
JWT authentication
Input validation
Email uniqueness validation
Administrator authorization
Resource ownership checks
Server-side user identity
Protected review operations
Cross-origin request configuration

Security rules must be enforced by the backend and must not rely only on frontend controls.

Current Development Priorities

The main remaining improvements are:

Isolated Part 3 test configuration
Complete JWT protection for review operations
Review ownership validation
Database-level duplicate review prevention
Dependency consistency
Full integration testing between Parts 3 and 4
Documentation synchronization
Author

Developed by Jamhalex as part of the Holberton School software engineering curriculum.

License

This repository is intended for educational use as part of the Holberton School curriculum.

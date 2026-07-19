# HBnB Project

## Overview

HBnB is a full-stack accommodation management project developed as
part of the Holberton School curriculum.

The project is divided into four progressive parts:

1. Software architecture and UML design
2. Business logic and REST API development
3. Authentication and database persistence
4. Frontend implementation and API integration

The application manages users, places, amenities, and reviews through
a layered architecture built with Flask.

---

## Repository Structure

```text
holbertonschool-hbnb/
├── part1/
│   ├── business-logic-layer.md
│   ├── business-logic-layer.mmd
│   ├── business-logic-layer.svg
│   ├── high-level-diagram.md
│   ├── high-level-diagram.mmd
│   ├── high-level-diagram.svg
│   ├── Amenity-Creation-Sequence.md
│   ├── Amenity-Creation-Sequence.mmd
│   ├── Amenity-Creation-Sequence.svg
│   ├── Place-Creation-Sequence.md
│   ├── Place-Creation-Sequence.mmd
│   ├── Place-Creation-Sequence.svg
│   ├── Review-Submission-Sequence.md
│   ├── Review-Submission-Sequence.mmd
│   ├── Review-Submission-Sequence.svg
│   ├── User-Registration-Sequence.md
│   ├── User-Registration-Sequence.mmd
│   ├── User-Registration-Sequence.svg
│   └── technical-documentation.md
│
├── part2/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── persistence/
│   │   └── services/
│   ├── docs/
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
│   ├── docs/
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

Part 1 defines the application architecture before implementation.

It includes:

A high-level package diagram
A business-logic class diagram
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

Part 3 extends the backend with authentication and relational
persistence.

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
CORS support for the frontend

Part 3 supports both the REST API and the Part 4 frontend.

Part 4 — Frontend

Part 4 provides a browser-based interface for the HBnB API.

Features include:

User login
JWT-based authentication
Place listing
Price filtering
Place details
Owner and amenity information
Review display
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

Each backend part has its own dependencies and should be installed
from its respective directory.

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

Current verified result:

24 passed
Running Part 3

Enter Part 3:

cd part3

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Optional development configuration:

export SECRET_KEY="your-development-secret"
export JWT_SECRET_KEY="your-jwt-secret"
export HBNB_ADMIN_EMAIL="admin@example.com"
export HBNB_ADMIN_PASSWORD="strong-password"

Start the API:

python3 run.py

The API documentation is available at:

http://127.0.0.1:5000/api/v1/

Run the tests:

pytest -q

Current verified result:

27 passed
Running Part 4

Start the Part 3 backend first.

From the repository root, serve the frontend:

cd part4
python3 -m http.server 8000

Open:

http://127.0.0.1:8000/

The frontend expects the API at:

http://127.0.0.1:5000/api/v1
Authentication

Part 3 uses JSON Web Tokens.

After a successful login, the API returns an access token:

{
  "access_token": "<jwt-token>"
}

Protected requests must include:

Authorization: Bearer <jwt-token>

The backend determines the authenticated user from the JWT identity.
Clients do not provide their own owner_id or user_id for protected
place and review creation.

Testing and Style

Run Part 2 checks:

cd part2
pytest -q
pycodestyle app tests

Run Part 3 checks:

cd part3
pytest -q
pycodestyle app tests

Check frontend JavaScript syntax:

node --check part4/scripts.js
Security Notes
Passwords are hashed with Flask-Bcrypt.
Password hashes are not included in API responses.
JWT identity determines resource ownership.
Administrative actions require an administrator claim.
Database writes roll back when SQLAlchemy operations fail.
Duplicate reviews are blocked by application logic and a database
uniqueness constraint.
Development secrets and administrator credentials should be replaced
before deploying the application.

Author

Johnson Alexander Martinez

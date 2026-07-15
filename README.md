# HBnB Project

## Overview

HBnB is a full-stack accommodation management platform developed as part of the Holberton School curriculum. The project follows a progressive architecture, beginning with object-oriented design and evolving into a secure REST API backed by a relational database.

Throughout the project, modern backend development concepts are implemented, including:

* Object-Oriented Programming (OOP)
* RESTful API design
* Flask Application Factory pattern
* JWT Authentication
* Password hashing with Bcrypt
* Repository and Facade design patterns
* SQLAlchemy ORM
* SQLite for development
* MySQL-ready architecture for production

---

# Repository Structure

```
holbertonschool-hbnb/
│
├── part1/
│   ├── Business logic layer
│   ├── Domain models
│   └── UML design
│
├── part2/
│   ├── REST API
│   ├── CRUD endpoints
│   ├── Swagger documentation
│   └── Unit tests
│
├── part3/
│   ├── JWT Authentication
│   ├── Role-based authorization
│   ├── SQLAlchemy integration
│   ├── SQLite persistence
│   └── Database-ready architecture
│
└── README.md
```

---

# Technologies

* Python 3
* Flask
* Flask-RESTX
* Flask-Bcrypt
* Flask-JWT-Extended
* Flask-SQLAlchemy
* SQLite
* MySQL (production ready)
* unittest
* pycodestyle

---

# Features

## User Management

* User registration
* Password hashing
* JWT login
* User profile management
* Administrator accounts

## Authentication

* Secure JWT authentication
* Token-based authorization
* Protected endpoints
* Administrator permissions

## Places

* Create places
* Update places
* Retrieve places
* Ownership validation

## Reviews

* Create reviews
* Update reviews
* Ownership validation
* Duplicate review prevention

## Amenities

* Create amenities
* Update amenities
* Administrator-only management

---

# Architecture

The project follows a layered architecture.

```
Presentation Layer
        │
        ▼
REST API (Flask-RESTX)
        │
        ▼
Facade Layer
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy ORM
        │
        ▼
SQLite / MySQL
```

---

# Design Patterns

* Application Factory
* Repository Pattern
* Facade Pattern
* ORM (SQLAlchemy)

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/holbertonschool-hbnb.git
```

Enter the project:

```bash
cd holbertonschool-hbnb
```

Choose the desired project part:

```bash
cd part3
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

```bash
python3 run.py
```

Default address:

```
http://127.0.0.1:5000
```

Swagger documentation:

```
http://127.0.0.1:5000/api/v1/
```

---

# Testing

Run unit tests:

```bash
python3 -m unittest discover
```

Run code style checks:

```bash
pycodestyle app
```

---

# Security

The project implements several security best practices:

* Password hashing using Bcrypt
* JWT authentication
* Role-based authorization
* Administrator privileges
* Input validation
* Protected API endpoints
* Email uniqueness validation

---

# Future Improvements

* Complete SQLAlchemy mapping for all entities
* MySQL production configuration
* Docker support
* CI/CD pipeline
* API rate limiting
* Refresh tokens
* Pagination and filtering
* Automated integration tests

---

# Authors

Developed as part of the Holberton School curriculum.

---

# License

This project is intended for educational purposes as part of the Holberton School software engineering program.


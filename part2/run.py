#!/usr/bin/python3
"""
Run the HBnB Flask application.
"""

from app import create_app
from app.services import facade


app = create_app()


def create_default_admin():
    """
    Create a development administrator if one does not already exist.
    """

    admin_email = "admin@test.com"

    existing_admin = facade.get_user_by_email(admin_email)

    if existing_admin:
        return

    facade.create_user({
        "first_name": "Admin",
        "last_name": "User",
        "email": admin_email,
        "password": "admin123",
        "is_admin": True
    })

    print("Development administrator created:")
    print("Email: admin@test.com")
    print("Password: admin123")


if __name__ == "__main__":
    create_default_admin()
    app.run(debug=True)

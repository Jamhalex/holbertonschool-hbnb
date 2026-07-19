#!/usr/bin/python3
"""
Run the HBnB Flask application.
"""

import os

from app import create_app
from app.extensions import db
from app.services import facade


app = create_app()


def create_default_admin():
    """
    Create a development administrator when one does not exist.

    Administrator credentials can be configured with environment
    variables.
    """

    admin_email = os.getenv(
        "HBNB_ADMIN_EMAIL",
        "admin@test.com"
    ).strip().lower()

    admin_password = os.getenv(
        "HBNB_ADMIN_PASSWORD",
        "admin123"
    )

    existing_admin = facade.get_user_by_email(
        admin_email
    )

    if existing_admin:
        return existing_admin

    admin = facade.create_user({
        "first_name": "Admin",
        "last_name": "User",
        "email": admin_email,
        "password": admin_password,
        "is_admin": True
    })

    print("Development administrator created:")
    print(f"Email: {admin_email}")

    return admin


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_admin()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=app.config.get("DEBUG", False),
        use_reloader=False
    )

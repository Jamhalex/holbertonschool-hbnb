#!/usr/bin/python3
"""
User model for HBnB application.
"""

from app.models.base_model import BaseModel
from app.extensions import bcrypt


class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None
    ):
        """
        Initialize a User instance.
        """

        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        self.password = None
        if password:
            self.hash_password(password)

        self.places = []
        self.reviews = []

    def hash_password(self, password):
        """
        Hash and store the user's password.
        """

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """
        Verify a password against the stored hash.
        """

        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def to_dict(self):
        """
        Return dictionary representation of the user.

        Password is intentionally excluded.
        """

        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        })

        return data

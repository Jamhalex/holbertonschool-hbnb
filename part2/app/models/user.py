#!/usr/bin/python3
"""
User model for HBnB application.
"""

from app.extensions import bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        """
        Initialize a User instance.

        Args:
            first_name (str): User first name.
            last_name (str): User last name.
            email (str): User email address.
            password (str, optional): Plain-text password to hash.
            is_admin (bool, optional): Administrator status.
        """

        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

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

        if not self.password:
            return False

        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def to_dict(self):
        """
        Return a dictionary representation of the user.

        The password is intentionally excluded.
        """

        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })

        return data

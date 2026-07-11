#!/usr/bin/python3
"""
User model for HBnB application.
"""

from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the HBnB application.
    """

    def __init__(self, first_name, last_name, email):
        """
        Initialize a User instance.

        Args:
            first_name (str): User first name.
            last_name (str): User last name.
            email (str): User email address.
        """

        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        # Relationships
        self.places = []
        self.reviews = []

    def to_dict(self):
        """
        Return dictionary representation of the user.
        """

        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        })

        return data

#!/usr/bin/python3
"""
User model for the HBnB application.
"""

from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represent a user in the HBnB application.
    """

    def __init__(self, first_name, last_name, email):
        """
        Initialize a User instance.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            email (str): User's unique email address.
        """

        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Associate a place with the user.

        Args:
            place (Place): Place owned by the user.
        """

        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """
        Associate a review with the user.

        Args:
            review (Review): Review written by the user.
        """

        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """
        Return a dictionary representation of the user.
        """

        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        })

        return data

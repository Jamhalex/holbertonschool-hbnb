#!/usr/bin/python3
"""
Review model for the HBnB application.
"""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Represent a review written by a user for a place.
    """

    def __init__(self, text, user, place):
        """
        Initialize a Review instance.

        Args:
            text (str): Review content.
            user (User): User who created the review.
            place (Place): Place being reviewed.
        """

        super().__init__()

        self.text = text
        self.user = user
        self.place = place

        place.add_review(self)
        user.add_review(self)

    def to_dict(self):
        """
        Return a dictionary representation of the review.
        """

        data = super().to_dict()

        data.update({
            "text": self.text,
            "user_id": self.user.id,
            "place_id": self.place.id
        })

        return data

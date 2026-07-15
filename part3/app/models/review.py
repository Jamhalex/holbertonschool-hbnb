#!/usr/bin/python3
"""
Review model for HBnB application.
"""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review entity.
    """

    def __init__(
        self,
        text,
        user,
        place
    ):
        """
        Initialize review.

        Args:
            text (str): Review content.
            user (User): User who created review.
            place (Place): Place being reviewed.
        """

        super().__init__()

        self.text = text
        self.user = user
        self.place = place

        # Maintain relationships
        place.add_review(self)
        user.reviews.append(self)

    def to_dict(self):
        """
        Serialize review object.
        """

        data = super().to_dict()

        data.update({
            "text": self.text,
            "user_id": self.user.id,
            "place_id": self.place.id
        })

        return data

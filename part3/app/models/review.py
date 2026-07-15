#!/usr/bin/python3
"""
Review model for the HBnB application.
"""

from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    SQLAlchemy model representing a review.
    """

    __tablename__ = "reviews"

    text = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="reviews"
    )

    place = db.relationship(
        "Place",
        back_populates="reviews"
    )

    def __init__(
        self,
        text,
        user_id,
        place_id
    ):
        """
        Initialize a Review instance.
        """

        self.text = text
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self):
        """
        Return a dictionary representation of the review.
        """

        data = super().to_dict()

        data.update({
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        return data

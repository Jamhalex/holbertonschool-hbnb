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

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "place_id",
            name="uq_review_user_place"
        ),
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False,
        index=True
    )

    user = db.relationship(
        "User",
        back_populates="reviews",
        lazy=True
    )

    place = db.relationship(
        "Place",
        back_populates="reviews",
        lazy=True
    )

    def __init__(
        self,
        text,
        user_id,
        place_id
    ):
        """
        Initialize a Review instance.

        Args:
            text (str): Review text.
            user_id (str): ID of the author.
            place_id (str): ID of the reviewed place.
        """

        self.text = text.strip()
        self.user_id = user_id
        self.place_id = place_id

    def update(self, data):
        """
        Update review attributes safely.
        """

        update_data = data.copy()

        if "text" in update_data:
            update_data["text"] = update_data[
                "text"
            ].strip()

        update_data.pop("user_id", None)
        update_data.pop("place_id", None)

        super().update(update_data)

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

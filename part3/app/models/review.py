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
        db.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_review_rating"
        )
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    rating = db.Column(
        db.Integer,
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
        rating,
        user_id,
        place_id
    ):
        """
        Initialize a Review instance.

        Args:
            text (str): Review text.
            rating (int): Rating from 1 through 5.
            user_id (str): ID of the author.
            place_id (str): ID of the reviewed place.
        """

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text is required")

        if isinstance(rating, bool) or not isinstance(rating, int):
            raise ValueError("Rating must be an integer")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        self.text = text.strip()
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def update(self, data):
        """
        Update review attributes safely.
        """

        update_data = data.copy()

        if "text" in update_data:
            text = update_data["text"]

            if not isinstance(text, str) or not text.strip():
                raise ValueError("Review text is required")

            update_data["text"] = text.strip()

        if "rating" in update_data:
            rating = update_data["rating"]

            if isinstance(rating, bool) or not isinstance(rating, int):
                raise ValueError("Rating must be an integer")

            if rating < 1 or rating > 5:
                raise ValueError(
                    "Rating must be between 1 and 5"
                )

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
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        return data

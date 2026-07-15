#!/usr/bin/python3
"""
Place model for the HBnB application.
"""

from app.extensions import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    SQLAlchemy model representing a place.
    """

    __tablename__ = "places"

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    owner_id = db.Column(
        db.String(36),
        nullable=False
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id
    ):
        """
        Initialize a Place instance.
        """

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def to_dict(self):
        """
        Return a dictionary representation of the place.
        """

        data = super().to_dict()

        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        })

        return data

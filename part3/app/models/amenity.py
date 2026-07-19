#!/usr/bin/python3
"""
Amenity model for the HBnB application.
"""

from app.extensions import db
from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


class Amenity(BaseModel):
    """
    SQLAlchemy model representing an amenity.
    """

    __tablename__ = "amenities"

    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        index=True
    )

    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
        lazy=True
    )

    def __init__(self, name):
        """
        Initialize an Amenity instance.

        Args:
            name (str): Amenity name.
        """

        self.name = name.strip()

    def update(self, data):
        """
        Update amenity attributes safely.
        """

        update_data = data.copy()

        if "name" in update_data:
            update_data["name"] = update_data[
                "name"
            ].strip()

        super().update(update_data)

    def to_dict(self):
        """
        Return a dictionary representation of the amenity.
        """

        data = super().to_dict()

        data.update({
            "name": self.name
        })

        return data

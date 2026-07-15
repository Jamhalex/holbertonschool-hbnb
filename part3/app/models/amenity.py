#!/usr/bin/python3
"""
Amenity model for the HBnB application.
"""

from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    SQLAlchemy model representing an amenity.
    """

    __tablename__ = "amenities"

    name = db.Column(
        db.String(50),
        nullable=False
    )

    def __init__(self, name):
        """
        Initialize an Amenity instance.
        """

        self.name = name

    def to_dict(self):
        """
        Return a dictionary representation of the amenity.
        """

        data = super().to_dict()

        data.update({
            "name": self.name
        })

        return data

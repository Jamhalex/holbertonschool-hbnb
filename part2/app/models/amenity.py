#!/usr/bin/python3
"""
Amenity model for the HBnB application.
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represent an amenity that can be associated with one or more places.
    """

    def __init__(self, name):
        """
        Initialize an Amenity instance.

        Args:
            name (str): Name of the amenity.
        """

        super().__init__()

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

#!/usr/bin/python3
"""
Place model for the HBnB application.
"""

from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Represent a property listed in the HBnB application.
    """

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        """
        Initialize a Place instance.

        Args:
            title (str): Place title.
            description (str): Place description.
            price (float): Price per night.
            latitude (float): Geographic latitude.
            longitude (float): Geographic longitude.
            owner (User): User who owns the place.
        """

        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

        owner.add_place(self)

    def add_review(self, review):
        """
        Associate a review with the place.

        Args:
            review (Review): Review associated with the place.
        """

        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Associate an amenity with the place.

        Args:
            amenity (Amenity): Amenity available at the place.
        """

        if amenity not in self.amenities:
            self.amenities.append(amenity)

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
            "owner_id": self.owner.id
        })

        return data

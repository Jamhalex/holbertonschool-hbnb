#!/usr/bin/python3
"""
Place model for the HBnB application.
"""

from app.extensions import db
from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


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
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    owner = db.relationship(
        "User",
        back_populates="places",
        lazy=True
    )

    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan",
        order_by="Review.created_at.desc()",
        lazy=True
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy=True
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

        self.title = title.strip()
        self.description = (
            description.strip()
            if description
            else ""
        )
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def add_amenity(self, amenity):
        """
        Associate an amenity with this place.
        """

        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """
        Remove an amenity from this place.
        """

        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, data):
        """
        Update place attributes safely.
        """

        update_data = data.copy()

        if "title" in update_data:
            update_data["title"] = update_data[
                "title"
            ].strip()

        if (
            "description" in update_data
            and update_data["description"] is not None
        ):
            update_data["description"] = update_data[
                "description"
            ].strip()

        update_data.pop("owner_id", None)

        super().update(update_data)

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
            "owner_id": self.owner_id,
            "amenities": [
                amenity.id
                for amenity in self.amenities
            ]
        })

        return data

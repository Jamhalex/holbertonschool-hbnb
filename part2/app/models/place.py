#!/usr/bin/python3
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from app.models.base import BaseModel


@dataclass
class Place(BaseModel):
    title: str = ""
    description: str = ""
    price: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0

    owner_id: str = ""  # User.id
    amenity_ids: List[str] = field(default_factory=list)  # [Amenity.id, ...]
    review_ids: List[str] = field(default_factory=list)  # [Review.id, ...]

    def validate(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")

        # price
        if not isinstance(self.price, (int, float)):
            raise TypeError("price must be a number")
        if float(self.price) <= 0:
            raise ValueError("price must be > 0")

        # lat/lon basic sanity (you can tighten if spec requires)
        if not isinstance(self.latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if not isinstance(self.longitude, (int, float)):
            raise TypeError("longitude must be a number")
        lat = float(self.latitude)
        lon = float(self.longitude)
        if lat < -90 or lat > 90:
            raise ValueError("latitude must be between -90 and 90")
        if lon < -180 or lon > 180:
            raise ValueError("longitude must be between -180 and 180")

        # relationships as IDs
        if not isinstance(self.owner_id, str) or not self.owner_id.strip():
            raise ValueError("owner_id is required")
        if not isinstance(self.amenity_ids, list) or any(not isinstance(x, str) for x in self.amenity_ids):
            raise TypeError("amenity_ids must be a list of strings")
        if not isinstance(self.review_ids, list) or any(not isinstance(x, str) for x in self.review_ids):
            raise TypeError("review_ids must be a list of strings")

        # remove duplicates (keeps stable order)
        seen = set()
        cleaned = []
        for a_id in self.amenity_ids:
            if a_id not in seen:
                seen.add(a_id)
                cleaned.append(a_id)
        self.amenity_ids = cleaned
        seen = set()
        cleaned = []
        for r_id in self.review_ids:
            if r_id not in seen:
                seen.add(r_id)
                cleaned.append(r_id)
        self.review_ids = cleaned

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "price": float(self.price),
                "latitude": float(self.latitude),
                "longitude": float(self.longitude),
                "owner_id": self.owner_id,
                "amenity_ids": list(self.amenity_ids),
                "review_ids": list(self.review_ids),
            }
        )
        return data

#!/usr/bin/python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from app.models.base import BaseModel


@dataclass
class Review(BaseModel):
    text: str = ""
    rating: Optional[int] = None

    user_id: str = ""   # User.id
    place_id: str = ""  # Place.id

    def validate(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text is required")

        if self.rating is not None:
            if not isinstance(self.rating, int):
                raise TypeError("rating must be an integer")
            if self.rating < 1 or self.rating > 5:
                raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.user_id, str) or not self.user_id.strip():
            raise ValueError("user_id is required")
        if not isinstance(self.place_id, str) or not self.place_id.strip():
            raise ValueError("place_id is required")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "text": self.text,
                "user_id": self.user_id,
                "place_id": self.place_id,
            }
        )
        if self.rating is not None:
            data["rating"] = self.rating
        return data

#!/usr/bin/python3
from __future__ import annotations

from dataclasses import dataclass
from app.models.base import BaseModel


@dataclass
class Amenity(BaseModel):
    name: str = ""

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["name"] = self.name
        return data

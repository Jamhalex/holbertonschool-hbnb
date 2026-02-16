#!/usr/bin/python3
from __future__ import annotations

from dataclasses import dataclass
from app.models.base import BaseModel


@dataclass
class User(BaseModel):
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    password: str = ""  # stored in-memory for now; DO NOT return in API

    def validate(self) -> None:
        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email is required")
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name is required")
        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name is required")
        if not isinstance(self.password, str) or not self.password.strip():
            raise ValueError("password is required")

    def to_dict(self) -> dict:
        # Intentionally exclude password
        data = super().to_dict()
        data.update(
            {
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
            }
        )
        return data

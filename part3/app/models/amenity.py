#!/usr/bin/python3

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity entity.
    """

    def __init__(self, name):
        super().__init__()

        self.name = name

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "name": self.name
        })

        return data

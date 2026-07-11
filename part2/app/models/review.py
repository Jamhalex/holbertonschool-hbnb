#!/usr/bin/python3

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review entity.
    """

    def __init__(
        self,
        text,
        user,
        place
    ):
        super().__init__()

        self.text = text
        self.user = user
        self.place = place

        place.add_review(self)
        user.reviews.append(self)

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "text": self.text,
            "user_id": self.user.id,
            "place_id": self.place.id
        })

        return data

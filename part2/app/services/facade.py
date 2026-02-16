#!/usr/bin/python3
from __future__ import annotations

from typing import Dict, List

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.persistence.repository import (
    ConflictError,
    InMemoryRepository,
    NotFoundError,
    ValidationError,
)


class HBnBFacade:
    def __init__(self, repo: InMemoryRepository) -> None:
        self.repo = repo

    # ---------- Users ----------
  
    def create_user(self, data: Dict) -> User:
        user = User(
            email=data.get("email", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            password=data.get("password", ""),
        )
        return self.repo.add(user)


    def list_users(self) -> List[User]:
        return self.repo.all(User)

    def get_user(self, user_id: str) -> User:
        return self.repo.get(User, user_id)

    def update_user(self, user_id: str, data: Dict) -> User:
        user = self.repo.get(User, user_id)
        updates = {}
        for k in ("email", "first_name", "last_name", "password"):
            if k in data:
                updates[k] = data[k]
        return self.repo.update(user, updates)

    # ---------- Amenities ----------
    def create_amenity(self, data: Dict) -> Amenity:
        amenity = Amenity(name=data.get("name", ""))
        return self.repo.add(amenity)

    def list_amenities(self) -> List[Amenity]:
        return self.repo.all(Amenity)

    def get_amenity(self, amenity_id: str) -> Amenity:
        return self.repo.get(Amenity, amenity_id)

    def update_amenity(self, amenity_id: str, data: Dict) -> Amenity:
        amenity = self.repo.get(Amenity, amenity_id)
        updates = {}
        if "name" in data:
            updates["name"] = data["name"]
        return self.repo.update(amenity, updates)

    def delete_amenity(self, amenity_id: str) -> None:
        self.repo.delete(Amenity, amenity_id)

    # ---------- Places ----------
    def create_place(self, data: Dict) -> Place:
        owner_id = data.get("owner_id", "")
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValidationError("owner_id is required")
        if not self.repo.exists(User, owner_id):
            raise NotFoundError("owner not found")

        amenity_ids = data.get("amenity_ids", [])
        if amenity_ids is None:
            amenity_ids = []
        if not isinstance(amenity_ids, list):
            raise ValidationError("amenity_ids must be a list")
        if any(not isinstance(a_id, str) for a_id in amenity_ids):
            raise ValidationError("amenity_ids must be a list of strings")
        for a_id in amenity_ids:
            if not self.repo.exists(Amenity, a_id):
                raise NotFoundError(f"amenity not found: {a_id}")

        place = Place(
            title=data.get("title", ""),
            description=data.get("description", ""),
            price=data.get("price", 0.0),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            owner_id=owner_id,
            amenity_ids=amenity_ids,
        )
        return self.repo.add(place)

    def list_places(self) -> List[Place]:
        return self.repo.all(Place)

    def get_place(self, place_id: str) -> Place:
        return self.repo.get(Place, place_id)

    def update_place(self, place_id: str, data: Dict) -> Place:
        place = self.repo.get(Place, place_id)

        updates: Dict = {}
        for k in ("title", "description", "price", "latitude", "longitude"):
            if k in data:
                updates[k] = data[k]

        if "owner_id" in data:
            owner_id = data["owner_id"]
            if not isinstance(owner_id, str) or not owner_id.strip():
                raise ValidationError("owner_id is required")
            if not self.repo.exists(User, owner_id):
                raise NotFoundError("owner not found")
            updates["owner_id"] = owner_id

        if "amenity_ids" in data:
            amenity_ids = data["amenity_ids"]
            if amenity_ids is None:
                amenity_ids = []
            if not isinstance(amenity_ids, list):
                raise ValidationError("amenity_ids must be a list")
            if any(not isinstance(a_id, str) for a_id in amenity_ids):
                raise ValidationError("amenity_ids must be a list of strings")
            for a_id in amenity_ids:
                if not self.repo.exists(Amenity, a_id):
                    raise NotFoundError(f"amenity not found: {a_id}")
            updates["amenity_ids"] = amenity_ids

        return self.repo.update(place, updates)

    # Extended serialization (owner + amenities)
    def place_to_extended_dict(self, place: Place) -> Dict:
        data = place.to_dict()
        owner = self.repo.get(User, place.owner_id)
        amenities = [self.repo.get(Amenity, a_id) for a_id in place.amenity_ids]
        reviews = [self.repo.get(Review, r_id) for r_id in place.review_ids if self.repo.exists(Review, r_id)]

        data["owner"] = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
        }
        data["amenities"] = [{"id": a.id, "name": a.name} for a in amenities]
        data["reviews"] = [r.to_dict() for r in reviews]
        return data

    # ---------- Reviews ----------
    def create_review(self, data: Dict) -> Review:
        text = data.get("text", "")
        if not isinstance(text, str) or not text.strip():
            raise ValidationError("text is required")

        user_id = data.get("user_id", "")
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValidationError("user_id is required")

        place_id = data.get("place_id", "")
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValidationError("place_id is required")

        if not self.repo.exists(User, user_id):
            raise NotFoundError("user not found")
        if not self.repo.exists(Place, place_id):
            raise NotFoundError("place not found")

        review = Review(
            text=text.strip(),
            rating=data.get("rating"),
            user_id=user_id,
            place_id=place_id,
        )
        review = self.repo.add(review)

        place = self.repo.get(Place, place_id)
        if review.id not in place.review_ids:
            review_ids = list(place.review_ids)
            review_ids.append(review.id)
            self.repo.update(place, {"review_ids": review_ids})

        return review

    def list_reviews(self) -> List[Review]:
        return self.repo.all(Review)

    def get_reviews(self) -> List[Review]:
        return self.list_reviews()

    def get_review(self, review_id: str) -> Review:
        return self.repo.get(Review, review_id)

    def update_review(self, review_id: str, data: Dict) -> Review:
        review = self.repo.get(Review, review_id)
        updates: Dict = {}
        if "text" in data:
            text = data.get("text", "")
            if not isinstance(text, str) or not text.strip():
                raise ValidationError("text is required")
            updates["text"] = text.strip()
        if not updates:
            return review
        return self.repo.update(review, updates)

    def delete_review(self, review_id: str) -> None:
        review = self.repo.get(Review, review_id)
        place_id = review.place_id
        if place_id and self.repo.exists(Place, place_id):
            place = self.repo.get(Place, place_id)
            review_ids = [r_id for r_id in place.review_ids if r_id != review_id]
            self.repo.update(place, {"review_ids": review_ids})
        self.repo.delete(Review, review_id)

    def get_reviews_for_place(self, place_id: str) -> List[Review]:
        place = self.repo.get(Place, place_id)
        return [self.repo.get(Review, r_id) for r_id in place.review_ids if self.repo.exists(Review, r_id)]

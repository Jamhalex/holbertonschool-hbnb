#!/usr/bin/python3
"""
Facade layer for the HBnB application.

Coordinates communication between:
- API layer
- Business logic layer
- Persistence layer
"""

from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    """
    Coordinate application operations through SQLAlchemy repositories.
    """

    def __init__(self):
        """
        Initialize SQLAlchemy repositories.
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # User operations

    def create_user(self, user_data):
        """
        Create and persist a user.
        """
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Retrieve all users.
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        """
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """
        Update and persist a user.
        """
        return self.user_repo.update(user_id, user_data)

    # Place operations

    def create_place(self, place_data):
        """
        Create and persist a place.

        Returns:
            Place: Newly created place, or None if validation fails.
        """
        owner_id = place_data.get("owner_id")

        if not self.user_repo.get(owner_id):
            return None

        amenities = []

        for amenity_id in place_data.get("amenity_ids", []):
            amenity = self.amenity_repo.get(amenity_id)

            if not amenity:
                return None

            amenities.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner_id
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        return self.place_repo.add(place)

    def get_place(self, place_id):
        """
        Retrieve a place by ID.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update and persist a place.

        Ownership cannot be changed through this method.
        """
        if not self.place_repo.get(place_id):
            return None

        update_data = place_data.copy()
        amenity_ids = update_data.pop("amenity_ids", None)
        update_data.pop("owner_id", None)

        amenities = None

        if amenity_ids is not None:
            amenities = []

            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)

                if not amenity:
                    return None

                amenities.append(amenity)

        place = self.place_repo.update(place_id, update_data)

        if not place:
            return None

        if amenities is not None:
            place.amenities = amenities
            place = self.place_repo.update(place_id, {})

        return place

    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Associate an amenity with a place.
        """
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)

        if not place or not amenity:
            return None

        place.add_amenity(amenity)
        return self.place_repo.update(place_id, {})

    def remove_amenity_from_place(self, place_id, amenity_id):
        """
        Remove an amenity from a place.
        """
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)

        if not place or not amenity:
            return None

        place.remove_amenity(amenity)
        return self.place_repo.update(place_id, {})

    # Amenity operations

    def create_amenity(self, amenity_data):
        """
        Create and persist an amenity.
        """
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        """
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by name.
        """
        if not isinstance(name, str) or not name.strip():
            return None

        return self.amenity_repo.get_by_attribute(
            "name",
            name.strip()
        )

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update and persist an amenity.
        """
        return self.amenity_repo.update(
            amenity_id,
            amenity_data
        )

    # Review operations

    def create_review(self, review_data):
        """
        Create and persist a review.

        A user may submit only one review for the same place.

        Returns:
            Review: Newly created review, or None if validation fails.
        """
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        text = review_data.get("text")
        rating = review_data.get("rating")

        if (
            not user_id
            or not place_id
            or not text
            or rating is None
        ):
            return None

        if not self.user_repo.get(user_id):
            return None

        if not self.place_repo.get(place_id):
            return None

        duplicate = (
            self.review_repo.get_review_by_user_and_place(
                user_id,
                place_id
            )
        )

        if duplicate:
            return None

        review = Review(
            text=text,
            rating=rating,
            user_id=user_id,
            place_id=place_id
        )

        return self.review_repo.add(review)

    def get_review(self, review_id):
        """
        Retrieve a review by ID.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """
        Update and persist a review.

        User and place associations cannot be changed.
        """
        update_data = review_data.copy()
        update_data.pop("user_id", None)
        update_data.pop("place_id", None)

        return self.review_repo.update(
            review_id,
            update_data
        )

    def delete_review(self, review_id):
        """
        Delete a review.
        """
        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a place.

        Returns:
            list: Place reviews, or None if the place does not exist.
        """
        if not self.place_repo.get(place_id):
            return None

        return self.review_repo.get_reviews_by_place(place_id)

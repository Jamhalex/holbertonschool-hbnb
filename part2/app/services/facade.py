#!/usr/bin/python3
"""
Facade layer for HBnB application.

Coordinates communication between:
- API layer
- Business logic layer
- Persistence layer
"""

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Main application facade.
    """

    def __init__(self):

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # =====================
    # User operations
    # =====================

    def create_user(self, user_data):

        user = User(**user_data)

        self.user_repo.add(user)

        return user

    def get_user(self, user_id):

        return self.user_repo.get(user_id)

    def get_all_users(self):

        return self.user_repo.get_all()

    def get_user_by_email(self, email):

        return self.user_repo.get_by_attribute(
            "email",
            email
        )

    def update_user(self, user_id, user_data):

        user = self.user_repo.get(user_id)

        if not user:
            return None

        user.update(user_data)

        return user

    # =====================
    # Place operations
    # =====================

    def create_place(self, place_data):

        owner = self.user_repo.get(
            place_data["owner_id"]
        )

        if not owner:
            return None

        place = Place(
            place_data["title"],
            place_data["description"],
            place_data["price"],
            place_data["latitude"],
            place_data["longitude"],
            owner
        )

        self.place_repo.add(place)

        return place

    def get_place(self, place_id):

        return self.place_repo.get(place_id)

    def get_all_places(self):

        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):

        place = self.place_repo.get(place_id)

        if not place:
            return None

        if "owner_id" in place_data:
            del place_data["owner_id"]

        place.update(place_data)

        return place

    # =====================
    # Amenity operations
    # =====================

    def create_amenity(self, amenity_data):

        amenity = Amenity(**amenity_data)

        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):

        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):

        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):

        amenity = self.amenity_repo.get(
            amenity_id
        )

        if not amenity:
            return None

        amenity.update(
            amenity_data
        )

        return amenity

    # =====================
    # Review operations
    # =====================

    def create_review(self, review_data):
        """
        Create a review.
        """

        review = Review(
            review_data["text"],
            review_data["user"],
            review_data["place"]
        )

        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        """
        Retrieve review by ID.
        """

        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.
        """

        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """
        Update review.
        """

        review = self.review_repo.get(review_id)

        if not review:
            return None

        review.update(review_data)

        return review

    def delete_review(self, review_id):
        """
        Delete review.
        """

        review = self.review_repo.get(review_id)

        if not review:
            return False

        self.review_repo.delete(review_id)

        return True

    def get_reviews_by_place(self, place_id):
        """
        Retrieve reviews for a place.
        """

        return [
            review
            for review in self.review_repo.get_all()
            if review.place.id == place_id
        ]

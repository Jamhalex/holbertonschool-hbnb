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
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Coordinate application operations through repositories.
    """

    def __init__(self):
        """
        Initialize the in-memory repositories.
        """

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User operations

    def create_user(self, user_data):
        """
        Create and store a user.

        Args:
            user_data (dict): User attributes.

        Returns:
            User: Newly created user.
        """

        user = User(**user_data)
        self.user_repo.add(user)

        return user

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

        return self.user_repo.get_by_attribute(
            "email",
            email
        )

    def update_user(self, user_id, user_data):
        """
        Update an existing user.
        """

        return self.user_repo.update(
            user_id,
            user_data
        )

    # Place operations

    def create_place(self, place_data):
        """
        Create and store a place.

        Args:
            place_data (dict): Place attributes.

        Returns:
            Place: Newly created place, or None if owner is missing.
        """

        owner = self.user_repo.get(
            place_data["owner_id"]
        )

        if not owner:
            return None

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        self.place_repo.add(place)

        return place

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
        Update an existing place.

        The owner cannot be changed through this operation.
        """

        update_data = place_data.copy()
        update_data.pop("owner_id", None)

        return self.place_repo.update(
            place_id,
            update_data
        )

    # Amenity operations

    def create_amenity(self, amenity_data):
        """
        Create and store an amenity.
        """

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)

        return amenity

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

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.
        """

        return self.amenity_repo.update(
            amenity_id,
            amenity_data
        )

    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Associate an amenity with a place.

        Returns:
            Place: Updated place, or None when either object is missing.
        """

        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)

        if not place or not amenity:
            return None

        place.add_amenity(amenity)

        return place

    # Review operations

    def create_review(self, review_data):
        """
        Create and store a review.

        Args:
            review_data (dict): Review text, user ID, and place ID.

        Returns:
            Review: Newly created review, or None if related data is missing.
        """

        user = self.user_repo.get(
            review_data["user_id"]
        )

        place = self.place_repo.get(
            review_data["place_id"]
        )

        if not user or not place:
            return None

        review = Review(
            text=review_data["text"],
            user=user,
            place=place
        )

        self.review_repo.add(review)

        return review

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
        Update an existing review.

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

        Returns:
            bool: True if deleted, otherwise False.
        """

        review = self.review_repo.get(review_id)

        if not review:
            return False

        if review in review.user.reviews:
            review.user.reviews.remove(review)

        if review in review.place.reviews:
            review.place.reviews.remove(review)

        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve reviews associated with a place.
        """

        place = self.place_repo.get(place_id)

        if not place:
            return None

        return list(place.reviews)

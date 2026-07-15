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
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    """
    Main application facade.
    """

    def __init__(self):
        """
        Initialize repositories.

        User persistence uses the user-specific SQLAlchemy repository.
        Other entities remain in memory until they are mapped.
        """

        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User operations

    def create_user(self, user_data):
        """
        Create and persist a user.
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

        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """
        Update and persist a user.
        """

        return self.user_repo.update(
            user_id,
            user_data
        )

    # Place operations

    def create_place(self, place_data):
        """
        Create a place owned by an existing user.
        """

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
        Update a place.
        """

        place_data = place_data.copy()
        place_data.pop("owner_id", None)

        return self.place_repo.update(
            place_id,
            place_data
        )

    # Amenity operations

    def create_amenity(self, amenity_data):
        """
        Create an amenity.
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
        Update an amenity.
        """

        return self.amenity_repo.update(
            amenity_id,
            amenity_data
        )

    # Review operations

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
        Update a review.
        """

        return self.review_repo.update(
            review_id,
            review_data
        )

    def delete_review(self, review_id):
        """
        Delete a review.
        """

        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a place.
        """

        return [
            review
            for review in self.review_repo.get_all()
            if review.place.id == place_id
        ]

#!/usr/bin/python3
"""
Facade layer for HBnB application.

The facade coordinates communication between:
- Presentation layer (API)
- Business Logic layer (Models)
- Persistence layer (Repositories)
"""

from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Facade class that manages application operations.
    """

    def __init__(self):
        """
        Initialize repositories for each entity.
        """

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # =====================
    # User operations
    # =====================

    def create_user(self, user_data):
        """
        Create and store a new user.

        Args:
            user_data (dict): User information.

        Returns:
            User: Created user object.
        """

        user = User(**user_data)
        self.user_repo.add(user)

        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): User UUID.

        Returns:
            User or None
        """

        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Retrieve all users.

        Returns:
            list: List of users.
        """

        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Retrieve user by email.

        Args:
            email (str): User email.

        Returns:
            User or None
        """

        return self.user_repo.get_by_attribute(
            "email",
            email
        )

    def update_user(self, user_id, user_data):
        """
        Update an existing user.

        Args:
            user_id (str): User UUID.
            user_data (dict): Updated fields.

        Returns:
            User or None
        """

        user = self.user_repo.get(user_id)

        if not user:
            return None

        user.update(user_data)

        return user


    # =====================
    # Place operations
    # =====================

    def get_place(self, place_id):
        """
        Retrieve a place by ID.

        Args:
            place_id (str): Place UUID.

        Returns:
            Place or None
        """

        return self.place_repo.get(place_id)


    # =====================
    # Amenity operations
    # =====================

    def create_amenity(self, amenity_data):
        """
        Create and store a new amenity.

        Args:
            amenity_data (dict): Amenity information.

        Returns:
            Amenity: Created amenity object.
        """

        amenity = Amenity(**amenity_data)

        self.amenity_repo.add(amenity)

        return amenity


    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): Amenity UUID.

        Returns:
            Amenity or None
        """

        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        """
        Retrieve all amenities.

        Returns:
            list: List of amenities.
        """

        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): Amenity UUID.
            amenity_data (dict): Updated fields.

        Returns:
            Amenity or None
        """

        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None

        amenity.update(amenity_data)

        return amenity

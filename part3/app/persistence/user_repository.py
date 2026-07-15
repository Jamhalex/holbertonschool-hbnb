#!/usr/bin/python3
"""
User-specific SQLAlchemy repository.
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User model operations.
    """

    def __init__(self):
        """
        Initialize the repository with the User model.
        """

        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.
        """

        return self.get_by_attribute(
            "email",
            email
        )

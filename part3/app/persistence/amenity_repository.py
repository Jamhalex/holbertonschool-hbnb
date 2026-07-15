#!/usr/bin/python3
"""
Amenity-specific SQLAlchemy repository.
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity model operations.
    """

    def __init__(self):
        """
        Initialize the repository with the Amenity model.
        """

        super().__init__(Amenity)

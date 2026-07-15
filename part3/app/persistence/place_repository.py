#!/usr/bin/python3
"""
Place-specific SQLAlchemy repository.
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place model operations.
    """

    def __init__(self):
        """
        Initialize the repository with the Place model.
        """

        super().__init__(Place)

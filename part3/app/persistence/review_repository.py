#!/usr/bin/python3
"""
Review-specific SQLAlchemy repository.
"""

from app.extensions import db
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review model operations.
    """

    def __init__(self):
        """
        Initialize the repository with the Review model.
        """

        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a place.
        """

        statement = db.select(Review).filter_by(
            place_id=place_id
        )

        return list(
            db.session.execute(statement).scalars()
        )

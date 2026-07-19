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

        Args:
            place_id (str): ID of the place.

        Returns:
            list: Reviews belonging to the specified place.
        """

        statement = (
            db.select(Review)
            .filter_by(place_id=place_id)
            .order_by(Review.created_at.desc())
        )

        return list(
            db.session.execute(
                statement
            ).scalars().all()
        )

    def get_review_by_user_and_place(
        self,
        user_id,
        place_id
    ):
        """
        Retrieve a review by a specific user for a specific place.

        Args:
            user_id (str): ID of the review author.
            place_id (str): ID of the reviewed place.

        Returns:
            Review | None: Matching review if it exists.
        """

        statement = (
            db.select(Review)
            .filter_by(
                user_id=user_id,
                place_id=place_id
            )
        )

        return db.session.execute(
            statement
        ).scalars().first()

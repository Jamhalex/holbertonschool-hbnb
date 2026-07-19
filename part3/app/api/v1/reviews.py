#!/usr/bin/python3
"""
Review API endpoints.
"""

from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.services import facade


api = Namespace(
    "reviews",
    description="Review operations"
)


review_model = api.model(
    "Review",
    {
        "text": fields.String(
            required=True,
            description="Review text"
        ),
        "rating": fields.Integer(
            required=True,
            min=1,
            max=5,
            description="Rating from 1 to 5"
        ),
        "place_id": fields.String(
            required=True,
            description="ID of the place being reviewed"
        )
    }
)


update_review_model = api.model(
    "UpdateReview",
    {
        "text": fields.String(
            required=False,
            description="Updated review text"
        ),
        "rating": fields.Integer(
            required=False,
            min=1,
            max=5,
            description="Updated rating from 1 to 5"
        )
    }
)


def serialize_user(user):
    """
    Return public information about a review author.
    """
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }


def serialize_review(review, include_user=False):
    """
    Return a dictionary representation of a review.

    Args:
        review (Review): Review to serialize.
        include_user (bool): Include public author information.

    Returns:
        dict: Serialized review data.
    """
    review_data = review.to_dict()

    if include_user and review.user:
        review_data["user"] = serialize_user(
            review.user
        )

    return review_data


def validate_review_data(review_data, require_place=True):
    """
    Validate review creation or update data.

    Args:
        review_data (dict): Review data to validate.
        require_place (bool): Whether place_id is required.

    Returns:
        tuple: Validation result and optional error message.
    """
    if not review_data:
        return False, "No review data provided"

    if require_place:
        allowed_fields = {
            "text",
            "rating",
            "place_id"
        }
        required_fields = {
            "text",
            "rating",
            "place_id"
        }
    else:
        allowed_fields = {
            "text",
            "rating"
        }
        required_fields = set()

    if not set(review_data).issubset(allowed_fields):
        return False, "Invalid review field"

    if not required_fields.issubset(review_data):
        return False, "Missing required review data"

    if not require_place and not set(review_data).intersection(
        allowed_fields
    ):
        return False, "No review data provided"

    if "text" in review_data:
        text = review_data.get("text")

        if not isinstance(text, str) or not text.strip():
            return False, "Review text is required"

    if "rating" in review_data:
        rating = review_data.get("rating")

        if isinstance(rating, bool) or not isinstance(rating, int):
            return False, "Rating must be an integer"

        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"

    if require_place:
        place_id = review_data.get("place_id")

        if not isinstance(place_id, str) or not place_id.strip():
            return False, "Place ID is required"

    return True, None


def can_modify_review(review):
    """
    Determine whether the authenticated user may modify a review.
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    return is_admin or review.user_id == current_user_id


@api.route("/")
class ReviewList(Resource):
    """
    Handle review collection operations.
    """

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(404, "Place not found")
    def post(self):
        """
        Create a review as the authenticated user.
        """
        review_data = api.payload.copy()

        valid, error = validate_review_data(
            review_data,
            require_place=True
        )

        if not valid:
            return {
                "error": error
            }, 400

        review_data["text"] = review_data[
            "text"
        ].strip()

        review_data["place_id"] = review_data[
            "place_id"
        ].strip()

        place = facade.get_place(
            review_data["place_id"]
        )

        if not place:
            return {
                "error": "Place not found"
            }, 404

        review_data["user_id"] = get_jwt_identity()

        try:
            review = facade.create_review(
                review_data
            )
        except (ValueError, SQLAlchemyError):
            return {
                "error": "Unable to create review"
            }, 400

        if not review:
            return {
                "error": (
                    "A review from this user already exists "
                    "for this place"
                )
            }, 400

        return serialize_review(
            review,
            include_user=True
        ), 201

    @api.response(200, "Reviews retrieved successfully")
    def get(self):
        """
        Retrieve all reviews.
        """
        reviews = facade.get_all_reviews()

        return [
            serialize_review(
                review,
                include_user=True
            )
            for review in reviews
        ], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    """
    Handle individual review operations.
    """

    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """
        Retrieve a review by ID.
        """
        review = facade.get_review(review_id)

        if not review:
            return {
                "error": "Review not found"
            }, 404

        return serialize_review(
            review,
            include_user=True
        ), 200

    @jwt_required()
    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """
        Update a review.

        Review authors may update their own reviews. Administrators may
        update any review.
        """
        review = facade.get_review(review_id)

        if not review:
            return {
                "error": "Review not found"
            }, 404

        if not can_modify_review(review):
            return {
                "error": "Unauthorized action"
            }, 403

        review_data = api.payload.copy()

        valid, error = validate_review_data(
            review_data,
            require_place=False
        )

        if not valid:
            return {
                "error": error
            }, 400

        if "text" in review_data:
            review_data["text"] = review_data[
                "text"
            ].strip()

        try:
            updated_review = facade.update_review(
                review_id,
                review_data
            )
        except (ValueError, SQLAlchemyError):
            return {
                "error": "Unable to update review"
            }, 400

        if not updated_review:
            return {
                "error": "Review not found"
            }, 404

        return serialize_review(
            updated_review,
            include_user=True
        ), 200

    @jwt_required()
    @api.response(200, "Review successfully deleted")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """
        Delete a review.

        Review authors may delete their own reviews. Administrators may
        delete any review.
        """
        review = facade.get_review(review_id)

        if not review:
            return {
                "error": "Review not found"
            }, 404

        if not can_modify_review(review):
            return {
                "error": "Unauthorized action"
            }, 403

        try:
            deleted = facade.delete_review(review_id)
        except SQLAlchemyError:
            return {
                "error": "Unable to delete review"
            }, 400

        if not deleted:
            return {
                "error": "Review not found"
            }, 404

        return {
            "message": "Review deleted successfully"
        }, 200


@api.route("/places/<place_id>")
class PlaceReviewList(Resource):
    """
    Handle reviews associated with a specific place.
    """

    @api.response(200, "Place reviews retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """
        Retrieve all reviews for a place.
        """
        reviews = facade.get_reviews_by_place(
            place_id
        )

        if reviews is None:
            return {
                "error": "Place not found"
            }, 404

        return [
            serialize_review(
                review,
                include_user=True
            )
            for review in reviews
        ], 200

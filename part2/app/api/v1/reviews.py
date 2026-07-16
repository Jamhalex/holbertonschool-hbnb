#!/usr/bin/python3
"""
Review API endpoints.
"""

from flask_restx import Namespace, Resource, fields

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
        "user_id": fields.String(
            required=True,
            description="ID of the user creating the review"
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
            required=True,
            description="Updated review text"
        )
    }
)


def validate_review_data(review_data, require_relationships=True):
    """
    Validate review creation or update data.

    Args:
        review_data (dict): Review data to validate.
        require_relationships (bool): Whether user and place IDs are required.

    Returns:
        tuple: Validation result and optional error message.
    """

    if not review_data:
        return False, "No review data provided"

    if require_relationships:
        allowed_fields = {
            "text",
            "user_id",
            "place_id"
        }

        required_fields = {
            "text",
            "user_id",
            "place_id"
        }
    else:
        allowed_fields = {
            "text"
        }

        required_fields = {
            "text"
        }

    if not set(review_data).issubset(allowed_fields):
        return False, "Invalid review field"

    if not required_fields.issubset(review_data):
        return False, "Missing required review data"

    text = review_data.get("text")

    if not isinstance(text, str) or not text.strip():
        return False, "Review text is required"

    if require_relationships:
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not isinstance(user_id, str) or not user_id.strip():
            return False, "User ID is required"

        if not isinstance(place_id, str) or not place_id.strip():
            return False, "Place ID is required"

    return True, None


def clean_review_data(review_data):
    """
    Trim whitespace from review string fields.
    """

    cleaned_data = review_data.copy()

    for field in ("text", "user_id", "place_id"):
        if field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip()

    return cleaned_data


@api.route("/")
class ReviewList(Resource):
    """
    Handle review collection operations.
    """

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or place not found")
    def post(self):
        """
        Create a new review.
        """

        review_data = api.payload.copy()

        valid, error = validate_review_data(
            review_data,
            require_relationships=True
        )

        if not valid:
            return {
                "error": error
            }, 400

        review_data = clean_review_data(review_data)

        user = facade.get_user(
            review_data["user_id"]
        )

        if not user:
            return {
                "error": "User not found"
            }, 404

        place = facade.get_place(
            review_data["place_id"]
        )

        if not place:
            return {
                "error": "Place not found"
            }, 404

        review = facade.create_review(
            review_data
        )

        if not review:
            return {
                "error": "Unable to create review"
            }, 400

        return review.to_dict(), 201

    @api.response(200, "Reviews retrieved successfully")
    def get(self):
        """
        Retrieve all reviews.
        """

        reviews = facade.get_all_reviews()

        return [
            review.to_dict()
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

        return review.to_dict(), 200

    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """
        Update the text of an existing review.
        """

        review = facade.get_review(review_id)

        if not review:
            return {
                "error": "Review not found"
            }, 404

        review_data = api.payload.copy()

        valid, error = validate_review_data(
            review_data,
            require_relationships=False
        )

        if not valid:
            return {
                "error": error
            }, 400

        review_data = clean_review_data(review_data)

        updated_review = facade.update_review(
            review_id,
            review_data
        )

        return updated_review.to_dict(), 200

    @api.response(200, "Review successfully deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """
        Delete a review.
        """

        deleted = facade.delete_review(review_id)

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
    Handle review retrieval for a specific place.
    """

    @api.response(200, "Place reviews retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """
        Retrieve all reviews associated with a place.
        """

        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {
                "error": "Place not found"
            }, 404

        return [
            review.to_dict()
            for review in reviews
        ], 200

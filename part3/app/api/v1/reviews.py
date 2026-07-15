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


@api.route("/")
class ReviewList(Resource):
    """
    Handle review collection operations.
    """

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created successfully")
    @api.response(400, "Invalid input data")
    def post(self):
        """
        Create a new review.
        """

        data = api.payload

        text = data.get("text")
        user_id = data.get("user_id")
        place_id = data.get("place_id")

        if not isinstance(text, str) or not text.strip():
            return {
                "error": "Review text is required"
            }, 400

        if not facade.get_user(user_id):
            return {
                "error": "User not found"
            }, 400

        if not facade.get_place(place_id):
            return {
                "error": "Place not found"
            }, 400

        review = facade.create_review({
            "text": text.strip(),
            "user_id": user_id,
            "place_id": place_id
        })

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
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """
        Update a review.
        """

        data = api.payload
        text = data.get("text")

        if not isinstance(text, str) or not text.strip():
            return {
                "error": "Review text is required"
            }, 400

        review = facade.update_review(
            review_id,
            {
                "text": text.strip()
            }
        )

        if not review:
            return {
                "error": "Review not found"
            }, 404

        return review.to_dict(), 200

    @api.response(200, "Review deleted successfully")
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

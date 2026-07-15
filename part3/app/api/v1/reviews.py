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


# Input / Swagger model
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


# =====================
# Reviews collection
# =====================

@api.route("/")
class ReviewList(Resource):
    """
    Handles review collection operations.
    """

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created successfully")
    @api.response(400, "Invalid input data")
    def post(self):
        """
        Create a new review.
        """

        data = api.payload

        # Validate text
        if not data.get("text"):
            return {
                "error": "Review text is required"
            }, 400

        # Find user
        user = facade.get_user(
            data["user_id"]
        )

        # Find place
        place = facade.get_place(
            data["place_id"]
        )

        if not user:
            return {
                "error": "User not found"
            }, 400

        if not place:
            return {
                "error": "Place not found"
            }, 400

        review = facade.create_review(
            {
                "text": data["text"],
                "user": user,
                "place": place
            }
        )

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


# =====================
# Single review
# =====================

@api.route("/<review_id>")
class ReviewResource(Resource):
    """
    Handles single review operations.
    """

    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """
        Retrieve review by ID.
        """

        review = facade.get_review(
            review_id
        )

        if not review:
            return {
                "error": "Review not found"
            }, 404

        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        """
        Update a review.
        """

        data = api.payload

        review = facade.update_review(
            review_id,
            data
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

        deleted = facade.delete_review(
            review_id
        )

        if not deleted:
            return {
                "error": "Review not found"
            }, 404

        return {
            "message": "Review deleted successfully"
        }, 200

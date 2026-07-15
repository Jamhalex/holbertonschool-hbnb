#!/usr/bin/python3
"""
Place API endpoints.
"""

from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace(
    "places",
    description="Place operations"
)


# ==========================
# PLACE CRETATION MODEL
# ==========================

place_model = api.model(
    "Place",
    {
        "title": fields.String(
            required=True,
            description="Place title"
        ),

        "description": fields.String(
            required=True,
            description="Place description"
        ),

        "price": fields.Float(
            required=True,
            description="Price per night"
        ),

        "latitude": fields.Float(
            required=True,
            description="Latitude"
        ),

        "longitude": fields.Float(
            required=True,
            description="Longitude"
        ),

        "owner_id": fields.String(
            required=True,
            description="Owner ID"
        )
    }
)


# ==========================
# PUT MODEL
# ==========================

update_place_model = api.model(
    "UpdatePlace",
    {
        "title": fields.String(
            description="Place title"
        ),

        "description": fields.String(
            description="Place description"
        ),

        "price": fields.Float(
            description="Price per night"
        ),

        "latitude": fields.Float(
            description="Latitude"
        ),

        "longitude": fields.Float(
            description="Longitude"
        )
    }
)


# ==========================
# PLACE COLLECTION
# ==========================

@api.route("/")
class PlaceList(Resource):
    """
    Handles place collection operations.
    """

    @api.expect(
        place_model,
        validate=True
    )
    @api.response(
        201,
        "Place successfully created"
    )
    @api.response(
        400,
        "Invalid input data"
    )
    @api.response(
        404,
        "Owner not found"
    )
    def post(self):
        """
        Create a new place.
        """

        place_data = api.payload

        # Validate title

        if not place_data["title"].strip():
            return {
                "error": "Title is required"
            }, 400

        # Validate description

        if not place_data["description"].strip():
            return {
                "error": "Description is required"
            }, 400

        # Validate price

        if place_data["price"] <= 0:
            return {
                "error":
                "Price must be greater than zero"
            }, 400

        # Validate latitude

        if not -90 <= place_data["latitude"] <= 90:
            return {
                "error":
                "Latitude must be between -90 and 90"
            }, 400

        # Validate longitude

        if not -180 <= place_data["longitude"] <= 180:
            return {
                "error":
                "Longitude must be between -180 and 180"
            }, 400

        place = facade.create_place(
            place_data
        )

        if not place:
            return {
                "error":
                "Owner not found"
            }, 404

        return place.to_dict(), 201

    @api.response(
        200,
        "Places retrieved successfully"
    )
    def get(self):
        """
        Retrieve all places.
        """

        places = facade.get_all_places()

        return [
            place.to_dict()
            for place in places
        ], 200


# ==========================
# SINGLE PLACE
# ==========================

@api.route(
    "/<place_id>"
)
class PlaceResource(Resource):
    """
    Handles individual place operations.
    """

    @api.response(
        200,
        "Place retrieved successfully"
    )
    @api.response(
        404,
        "Place not found"
    )
    def get(self, place_id):
        """
        Retrieve place by ID.
        """

        place = facade.get_place(
            place_id
        )

        if not place:
            return {
                "error":
                "Place not found"
            }, 404

        return place.to_dict(), 200

    @api.expect(
        update_place_model,
        validate=True
    )
    @api.response(
        200,
        "Place updated successfully"
    )
    @api.response(
        400,
        "Invalid input data"
    )
    @api.response(
        404,
        "Place not found"
    )
    def put(self, place_id):
        """
        Update a place.
        """

        place_data = api.payload

        # Validate title

        if "title" in place_data:
            if not place_data["title"].strip():
                return {
                    "error":
                    "Title cannot be empty"
                }, 400

        # Validate description

        if "description" in place_data:
            if not place_data["description"].strip():
                return {
                    "error":
                    "Description cannot be empty"
                }, 400

        # Validate price

        if "price" in place_data:
            if place_data["price"] <= 0:
                return {
                    "error":
                    "Price must be greater than zero"
                }, 400

        # Validate latitude

        if "latitude" in place_data:
            if not -90 <= place_data["latitude"] <= 90:
                return {
                    "error":
                    "Latitude must be between -90 and 90"
                }, 400

        # Validate longitude

        if "longitude" in place_data:
            if not -180 <= place_data["longitude"] <= 180:
                return {
                    "error":
                    "Longitude must be between -180 and 180"
                }, 400

        # Prevent owner changes

        if "owner_id" in place_data:
            del place_data["owner_id"]

        place = facade.update_place(
            place_id,
            place_data
        )

        if not place:
            return {
                "error":
                "Place not found"
            }, 404

        return place.to_dict(), 200

#!/usr/bin/python3
"""
Amenity API endpoints.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace(
    "amenities",
    description="Amenity operations"
)


# Define Amenity model for Swagger documentation
amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Name of the amenity"
        )
    }
)


@api.route("/")
class AmenityList(Resource):
    """
    Handles collection of amenities.
    """

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """
        Register a new amenity.
        """

        amenity_data = api.payload

        # Validate name
        if not amenity_data.get("name"):
            return {
                "error": "Amenity name is required"
            }, 400

        amenity = facade.create_amenity(
            amenity_data
        )

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """
        Retrieve all amenities.
        """

        amenities = facade.get_all_amenities()

        return [
            {
                "id": amenity.id,
                "name": amenity.name
            }
            for amenity in amenities
        ], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    """
    Handles individual amenity operations.
    """

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """
        Retrieve an amenity by ID.
        """

        amenity = facade.get_amenity(
            amenity_id
        )

        if not amenity:
            return {
                "error": "Amenity not found"
            }, 404

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """
        Update an amenity.
        """

        amenity_data = api.payload

        # Validate name
        if not amenity_data.get("name"):
            return {
                "error": "Amenity name is required"
            }, 400

        amenity = facade.update_amenity(
            amenity_id,
            amenity_data
        )

        if not amenity:
            return {
                "error": "Amenity not found"
            }, 404

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200

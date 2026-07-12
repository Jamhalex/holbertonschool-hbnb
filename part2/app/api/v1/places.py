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


@api.route("/")
class PlaceList(Resource):
    """
    Handles place collection operations.
    """

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """
        Create a new place.
        """

        place_data = api.payload


        # Validate price
        if place_data["price"] <= 0:
            return {
                "error": "Price must be greater than zero"
            }, 400


        # Validate latitude
        if not -90 <= place_data["latitude"] <= 90:
            return {
                "error": "Latitude must be between -90 and 90"
            }, 400


        # Validate longitude
        if not -180 <= place_data["longitude"] <= 180:
            return {
                "error": "Longitude must be between -180 and 180"
            }, 400


        place = facade.create_place(place_data)


        if not place:
            return {
                "error": "Owner not found"
            }, 404


        return place.to_dict(), 201



    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """
        Retrieve all places.
        """

        places = facade.get_all_places()

        return [
            place.to_dict()
            for place in places
        ], 200



@api.route("/<place_id>")
class PlaceResource(Resource):
    """
    Handles individual place operations.
    """


    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """
        Retrieve a place by ID.
        """

        place = facade.get_place(place_id)


        if not place:
            return {
                "error": "Place not found"
            }, 404


        return place.to_dict(), 200



    @api.expect(place_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """
        Update a place.
        """

        place_data = api.payload


        if "price" in place_data:
            if place_data["price"] <= 0:
                return {
                    "error": "Price must be greater than zero"
                }, 400


        if "latitude" in place_data:
            if not -90 <= place_data["latitude"] <= 90:
                return {
                    "error": "Invalid latitude"
                }, 400


        if "longitude" in place_data:
            if not -180 <= place_data["longitude"] <= 180:
                return {
                    "error": "Invalid longitude"
                }, 400



        place = facade.update_place(
            place_id,
            place_data
        )


        if not place:
            return {
                "error": "Place not found"
            }, 404


        return place.to_dict(), 200

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


update_place_model = api.model(
    "UpdatePlace",
    {
        "title": fields.String(
            description="Updated place title"
        ),
        "description": fields.String(
            description="Updated place description"
        ),
        "price": fields.Float(
            description="Updated price per night"
        ),
        "latitude": fields.Float(
            description="Updated latitude"
        ),
        "longitude": fields.Float(
            description="Updated longitude"
        )
    }
)


def validate_place_data(place_data, require_all=True):
    """
    Validate place creation or update data.

    Args:
        place_data (dict): Place data to validate.
        require_all (bool): Whether all creation fields are required.

    Returns:
        tuple: Validation result and optional error message.
    """

    allowed_fields = {
        "title",
        "description",
        "price",
        "latitude",
        "longitude",
        "owner_id"
    }

    if not place_data:
        return False, "No place data provided"

    if not set(place_data).issubset(allowed_fields):
        return False, "Invalid place field"

    required_fields = {
        "title",
        "description",
        "price",
        "latitude",
        "longitude",
        "owner_id"
    }

    if require_all and not required_fields.issubset(place_data):
        return False, "Missing required place data"

    if "title" in place_data:
        title = place_data["title"]

        if not isinstance(title, str) or not title.strip():
            return False, "Title is required"

    if "description" in place_data:
        description = place_data["description"]

        if (
            not isinstance(description, str)
            or not description.strip()
        ):
            return False, "Description is required"

    if "price" in place_data:
        price = place_data["price"]

        if not isinstance(price, (int, float)) or price <= 0:
            return False, "Price must be greater than zero"

    if "latitude" in place_data:
        latitude = place_data["latitude"]

        if (
            not isinstance(latitude, (int, float))
            or not -90 <= latitude <= 90
        ):
            return False, "Latitude must be between -90 and 90"

    if "longitude" in place_data:
        longitude = place_data["longitude"]

        if (
            not isinstance(longitude, (int, float))
            or not -180 <= longitude <= 180
        ):
            return False, "Longitude must be between -180 and 180"

    if "owner_id" in place_data:
        owner_id = place_data["owner_id"]

        if not isinstance(owner_id, str) or not owner_id.strip():
            return False, "Owner ID is required"

    return True, None


def clean_place_data(place_data):
    """
    Trim whitespace from place string fields.
    """

    cleaned_data = place_data.copy()

    for field in ("title", "description", "owner_id"):
        if field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip()

    return cleaned_data


@api.route("/")
class PlaceList(Resource):
    """
    Handle place collection operations.
    """

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """
        Create a new place.
        """

        place_data = api.payload.copy()

        valid, error = validate_place_data(
            place_data,
            require_all=True
        )

        if not valid:
            return {
                "error": error
            }, 400

        place_data = clean_place_data(place_data)

        place = facade.create_place(place_data)

        if not place:
            return {
                "error": "Owner not found"
            }, 404

        return place.to_dict(), 201

    @api.response(200, "Places retrieved successfully")
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
    Handle individual place operations.
    """

    @api.response(200, "Place retrieved successfully")
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

    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """
        Update a place.
        """

        place = facade.get_place(place_id)

        if not place:
            return {
                "error": "Place not found"
            }, 404

        place_data = api.payload.copy()

        valid, error = validate_place_data(
            place_data,
            require_all=False
        )

        if not valid:
            return {
                "error": error
            }, 400

        place_data = clean_place_data(place_data)

        place_data.pop("owner_id", None)

        updated_place = facade.update_place(
            place_id,
            place_data
        )

        return updated_place.to_dict(), 200

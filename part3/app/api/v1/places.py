#!/usr/bin/python3
"""
Place API endpoints.
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
        "amenity_ids": fields.List(
            fields.String,
            description="IDs of amenities associated with the place"
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
        ),
        "amenity_ids": fields.List(
            fields.String,
            description="Updated amenity IDs"
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

    if not place_data:
        return False, "No place data provided"

    allowed_fields = {
        "title",
        "description",
        "price",
        "latitude",
        "longitude",
        "amenity_ids"
    }

    if not set(place_data).issubset(allowed_fields):
        return False, "Invalid place field"

    required_fields = {
        "title",
        "description",
        "price",
        "latitude",
        "longitude"
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

        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price <= 0
        ):
            return False, "Price must be greater than zero"

    if "latitude" in place_data:
        latitude = place_data["latitude"]

        if (
            isinstance(latitude, bool)
            or not isinstance(latitude, (int, float))
            or not -90 <= latitude <= 90
        ):
            return False, "Latitude must be between -90 and 90"

    if "longitude" in place_data:
        longitude = place_data["longitude"]

        if (
            isinstance(longitude, bool)
            or not isinstance(longitude, (int, float))
            or not -180 <= longitude <= 180
        ):
            return False, "Longitude must be between -180 and 180"

    if "amenity_ids" in place_data:
        amenity_ids = place_data["amenity_ids"]

        if not isinstance(amenity_ids, list):
            return False, "amenity_ids must be a list"

        if not all(
            isinstance(amenity_id, str)
            and amenity_id.strip()
            for amenity_id in amenity_ids
        ):
            return False, "Every amenity ID must be a non-empty string"

        if len(amenity_ids) != len(set(amenity_ids)):
            return False, "Duplicate amenity IDs are not allowed"

    return True, None


def clean_place_data(place_data):
    """
    Normalize place data before persistence.
    """

    cleaned_data = place_data.copy()

    if "title" in cleaned_data:
        cleaned_data["title"] = cleaned_data[
            "title"
        ].strip()

    if "description" in cleaned_data:
        cleaned_data["description"] = cleaned_data[
            "description"
        ].strip()

    if "amenity_ids" in cleaned_data:
        cleaned_data["amenity_ids"] = [
            amenity_id.strip()
            for amenity_id in cleaned_data["amenity_ids"]
        ]

    return cleaned_data


def serialize_user(user):
    """
    Return public owner or reviewer information.
    """

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


def serialize_review(review):
    """
    Return review information for place details.
    """

    review_data = review.to_dict()

    if review.user:
        review_data["user"] = serialize_user(review.user)

    return review_data


def serialize_place(place, include_details=False):
    """
    Serialize a place.

    Args:
        place (Place): Place to serialize.
        include_details (bool): Include related entity details.

    Returns:
        dict: Serialized place data.
    """

    place_data = place.to_dict()

    if not include_details:
        return place_data

    place_data["owner"] = (
        serialize_user(place.owner)
        if place.owner
        else None
    )

    place_data["amenities"] = [
        amenity.to_dict()
        for amenity in place.amenities
    ]

    place_data["reviews"] = [
        serialize_review(review)
        for review in place.reviews
    ]

    return place_data


def can_modify_place(place):
    """
    Determine whether the authenticated user may modify a place.
    """

    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    return is_admin or place.owner_id == current_user_id


@api.route("/")
class PlaceList(Resource):
    """
    Handle place collection operations.
    """

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    def post(self):
        """
        Create a place owned by the authenticated user.
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

        place_data["owner_id"] = get_jwt_identity()

        try:
            place = facade.create_place(place_data)
        except SQLAlchemyError:
            return {
                "error": "Unable to create place"
            }, 400

        if not place:
            return {
                "error": "Owner or amenity not found"
            }, 400

        return serialize_place(
            place,
            include_details=True
        ), 201

    @api.response(200, "Places retrieved successfully")
    def get(self):
        """
        Retrieve all places.
        """

        places = facade.get_all_places()

        return [
            serialize_place(place)
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
        Retrieve detailed place information.
        """

        place = facade.get_place(place_id)

        if not place:
            return {
                "error": "Place not found"
            }, 404

        return serialize_place(
            place,
            include_details=True
        ), 200

    @jwt_required()
    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """
        Update a place.

        Owners may modify their own places. Administrators may modify
        any place.
        """

        place = facade.get_place(place_id)

        if not place:
            return {
                "error": "Place not found"
            }, 404

        if not can_modify_place(place):
            return {
                "error": "Unauthorized action"
            }, 403

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

        try:
            updated_place = facade.update_place(
                place_id,
                place_data
            )
        except SQLAlchemyError:
            return {
                "error": "Unable to update place"
            }, 400

        if not updated_place:
            return {
                "error": "Amenity not found"
            }, 400

        return serialize_place(
            updated_place,
            include_details=True
        ), 200

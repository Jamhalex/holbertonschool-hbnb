#!/usr/bin/python3
"""
Amenity API endpoints.
"""

from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.services import facade


api = Namespace(
    "amenities",
    description="Amenity operations"
)


amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Name of the amenity"
        )
    }
)


def serialize_amenity(amenity):
    """
    Return a dictionary representation of an amenity.
    """

    return amenity.to_dict()


def validate_amenity_data(amenity_data):
    """
    Validate amenity request data.

    Args:
        amenity_data (dict): Amenity data to validate.

    Returns:
        tuple: Validation result and optional error message.
    """

    if not amenity_data:
        return False, "No amenity data provided"

    if set(amenity_data) != {"name"}:
        return False, "Invalid amenity field"

    name = amenity_data.get("name")

    if not isinstance(name, str) or not name.strip():
        return False, "Amenity name is required"

    return True, None


def administrator_required():
    """
    Check whether the current JWT belongs to an administrator.

    Returns:
        bool: True when the current user is an administrator.
    """

    claims = get_jwt()

    return bool(claims.get("is_admin", False))


@api.route("/")
class AmenityList(Resource):
    """
    Handle amenity collection operations.
    """

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Administrator access required")
    def post(self):
        """
        Create a new amenity as an administrator.
        """

        if not administrator_required():
            return {
                "error": "Administrator access required"
            }, 403

        amenity_data = api.payload.copy()

        valid, error = validate_amenity_data(
            amenity_data
        )

        if not valid:
            return {
                "error": error
            }, 400

        amenity_data["name"] = amenity_data[
            "name"
        ].strip()

        existing_amenity = facade.get_amenity_by_name(
            amenity_data["name"]
        )

        if existing_amenity:
            return {
                "error": "Amenity already exists"
            }, 400

        try:
            amenity = facade.create_amenity(
                amenity_data
            )
        except SQLAlchemyError:
            return {
                "error": "Unable to create amenity"
            }, 400

        return serialize_amenity(amenity), 201

    @api.response(200, "Amenities retrieved successfully")
    def get(self):
        """
        Retrieve all amenities.
        """

        amenities = facade.get_all_amenities()

        return [
            serialize_amenity(amenity)
            for amenity in amenities
        ], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    """
    Handle individual amenity operations.
    """

    @api.response(200, "Amenity retrieved successfully")
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

        return serialize_amenity(amenity), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Administrator access required")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """
        Update an amenity as an administrator.
        """

        if not administrator_required():
            return {
                "error": "Administrator access required"
            }, 403

        amenity = facade.get_amenity(
            amenity_id
        )

        if not amenity:
            return {
                "error": "Amenity not found"
            }, 404

        amenity_data = api.payload.copy()

        valid, error = validate_amenity_data(
            amenity_data
        )

        if not valid:
            return {
                "error": error
            }, 400

        amenity_data["name"] = amenity_data[
            "name"
        ].strip()

        existing_amenity = facade.get_amenity_by_name(
            amenity_data["name"]
        )

        if (
            existing_amenity
            and existing_amenity.id != amenity_id
        ):
            return {
                "error": "Amenity already exists"
            }, 400

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                amenity_data
            )
        except SQLAlchemyError:
            return {
                "error": "Unable to update amenity"
            }, 400

        return serialize_amenity(updated_amenity), 200

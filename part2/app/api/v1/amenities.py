#!/usr/bin/python3
from flask import current_app, request
from flask_restx import Namespace, Resource

from app.persistence.repository import ConflictError, NotFoundError, ValidationError

api = Namespace("amenities", description="Amenity operations")


def facade():
    return current_app.config["FACADE"]


@api.route("/")
class AmenityList(Resource):
    def get(self):
        amenities = [a.to_dict() for a in facade().list_amenities()]
        return amenities, 200

    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            amenity = facade().create_amenity(payload)
            return amenity.to_dict(), 201
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409


@api.route("/<string:amenity_id>")
class AmenityItem(Resource):
    def get(self, amenity_id):
        try:
            amenity = facade().get_amenity(amenity_id)
            return amenity.to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404

    def put(self, amenity_id):
        payload = request.get_json(silent=True) or {}
        try:
            amenity = facade().update_amenity(amenity_id, payload)
            return amenity.to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409

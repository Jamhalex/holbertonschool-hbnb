#!/usr/bin/python3
from flask import current_app, request
from flask_restx import Namespace, Resource
from app.persistence.repository import ConflictError, NotFoundError, ValidationError

api = Namespace("places", description="Place operations")


def facade():
    return current_app.config["FACADE"]


@api.route("/")
class PlaceList(Resource):
    def get(self):
        # Basic list (no extended composition needed here)
        return [p.to_dict() for p in facade().list_places()], 200

    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            p = facade().create_place(payload)
            return p.to_dict(), 201
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409


@api.route("/<string:place_id>")
class PlaceItem(Resource):
    def get(self, place_id):
        try:
            p = facade().get_place(place_id)
            # Extended details: owner + amenities
            return facade().place_to_extended_dict(p), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404

    def put(self, place_id):
        payload = request.get_json(silent=True) or {}
        try:
            p = facade().update_place(place_id, payload)
            return p.to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409

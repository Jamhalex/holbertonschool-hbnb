#!/usr/bin/python3
from flask import current_app, request
from flask_restx import Namespace, Resource

from app.persistence.repository import ConflictError, NotFoundError, ValidationError

api = Namespace("users", description="User operations")


def facade():
    return current_app.config["FACADE"]


@api.route("/")
class UserList(Resource):
    def get(self):
        users = [u.to_dict() for u in facade().list_users()]
        return users, 200

    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            user = facade().create_user(payload)
            return user.to_dict(), 201
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409


@api.route("/<string:user_id>")
class UserItem(Resource):
    def get(self, user_id):
        try:
            user = facade().get_user(user_id)
            return user.to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404

    def put(self, user_id):
        payload = request.get_json(silent=True) or {}
        try:
            user = facade().update_user(user_id, payload)
            return user.to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409

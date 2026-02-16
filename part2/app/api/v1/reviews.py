#!/usr/bin/python3
from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from app.persistence.repository import ConflictError, NotFoundError, ValidationError

api = Namespace("reviews", description="Review operations")

review_create = api.model(
    "ReviewCreate",
    {
        "text": fields.String(required=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
        "rating": fields.Integer(required=False),
    },
)
review_update = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(required=True),
    },
)


def facade():
    return current_app.config["FACADE"]


@api.route("/")
class ReviewList(Resource):
    def get(self):
        return [r.to_dict() for r in facade().list_reviews()], 200

    @api.expect(review_create, validate=True)
    def post(self):
        payload = request.get_json(silent=True) or {}
        try:
            r = facade().create_review(payload)
            return r.to_dict(), 201
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409


@api.route("/<string:review_id>")
class ReviewItem(Resource):
    def get(self, review_id):
        try:
            return facade().get_review(review_id).to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404

    @api.expect(review_update, validate=True)
    def put(self, review_id):
        payload = request.get_json(silent=True) or {}
        try:
            return facade().update_review(review_id, payload).to_dict(), 200
        except NotFoundError as e:
            return {"error": str(e)}, 404
        except ValidationError as e:
            return {"error": str(e)}, 400
        except ConflictError as e:
            return {"error": str(e)}, 409

    def delete(self, review_id):
        try:
            facade().delete_review(review_id)
            return "", 204
        except NotFoundError as e:
            return {"error": str(e)}, 404

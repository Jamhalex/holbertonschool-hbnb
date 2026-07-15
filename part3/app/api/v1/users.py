#!/usr/bin/python3
"""
User API endpoints.
"""

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace(
    "users",
    description="User operations"
)


user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user"
        ),
        "email": fields.String(
            required=True,
            description="Email of the user"
        ),
        "password": fields.String(
            required=True,
            description="User password"
        ),
        "is_admin": fields.Boolean(
            description="Administrator status",
            default=False
        )
    }
)


update_user_model = api.model(
    "UpdateUser",
    {
        "first_name": fields.String(
            description="Updated first name"
        ),
        "last_name": fields.String(
            description="Updated last name"
        ),
        "email": fields.String(
            description="Updated email address"
        ),
        "password": fields.String(
            description="Updated password"
        ),
        "is_admin": fields.Boolean(
            description="Updated administrator status"
        )
    }
)


def serialize_user(user):
    """
    Return public user data without exposing the password.
    """

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin
    }


def validate_registration_data(user_data):
    """
    Validate user creation input.
    """

    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    email = user_data.get("email")
    password = user_data.get("password")

    if not isinstance(first_name, str) or not first_name.strip():
        return False, "First name is required"

    if not isinstance(last_name, str) or not last_name.strip():
        return False, "Last name is required"

    if not isinstance(email, str) or not email.strip():
        return False, "Email is required"

    if "@" not in email:
        return False, "Invalid email format"

    if not isinstance(password, str) or not password.strip():
        return False, "Password is required"

    if (
        "is_admin" in user_data
        and not isinstance(user_data["is_admin"], bool)
    ):
        return False, "is_admin must be a boolean"

    return True, None


def validate_regular_update(user_data):
    """
    Validate fields a regular user may update.
    """

    if not user_data:
        return False, "No update data provided"

    allowed_fields = {
        "first_name",
        "last_name"
    }

    if not set(user_data).issubset(allowed_fields):
        return (
            False,
            "Regular users may only update first_name and last_name"
        )

    if "first_name" in user_data:
        first_name = user_data["first_name"]

        if not isinstance(first_name, str) or not first_name.strip():
            return False, "First name cannot be empty"

    if "last_name" in user_data:
        last_name = user_data["last_name"]

        if not isinstance(last_name, str) or not last_name.strip():
            return False, "Last name cannot be empty"

    return True, None


def validate_admin_update(user_data):
    """
    Validate fields an administrator may update.
    """

    if not user_data:
        return False, "No update data provided"

    allowed_fields = {
        "first_name",
        "last_name",
        "email",
        "password",
        "is_admin"
    }

    if not set(user_data).issubset(allowed_fields):
        return False, "Invalid update field"

    if "first_name" in user_data:
        first_name = user_data["first_name"]

        if not isinstance(first_name, str) or not first_name.strip():
            return False, "First name cannot be empty"

    if "last_name" in user_data:
        last_name = user_data["last_name"]

        if not isinstance(last_name, str) or not last_name.strip():
            return False, "Last name cannot be empty"

    if "email" in user_data:
        email = user_data["email"]

        if not isinstance(email, str) or not email.strip():
            return False, "Email cannot be empty"

        if "@" not in email:
            return False, "Invalid email format"

    if "password" in user_data:
        password = user_data["password"]

        if not isinstance(password, str) or not password.strip():
            return False, "Password cannot be empty"

    if (
        "is_admin" in user_data
        and not isinstance(user_data["is_admin"], bool)
    ):
        return False, "is_admin must be a boolean"

    return True, None


@api.route("/")
class UserList(Resource):
    """
    Handle user collection operations.
    """

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Administrator access required")
    def post(self):
        """
        Create a new user as an administrator.
        """

        claims = get_jwt()

        if not claims.get("is_admin", False):
            return {
                "error": "Administrator access required"
            }, 403

        user_data = api.payload.copy()

        valid, error = validate_registration_data(user_data)

        if not valid:
            return {
                "error": error
            }, 400

        email = user_data["email"].strip()

        existing_user = facade.get_user_by_email(email)

        if existing_user:
            return {
                "error": "Email already registered"
            }, 400

        user_data["first_name"] = user_data["first_name"].strip()
        user_data["last_name"] = user_data["last_name"].strip()
        user_data["email"] = email

        new_user = facade.create_user(user_data)

        return serialize_user(new_user), 201

    @api.response(200, "Users retrieved successfully")
    def get(self):
        """
        Retrieve all users.
        """

        users = facade.get_all_users()

        return [
            serialize_user(user)
            for user in users
        ], 200


@api.route("/<user_id>")
class UserResource(Resource):
    """
    Handle individual user operations.
    """

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """
        Retrieve a user by ID.
        """

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        return serialize_user(user), 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    def put(self, user_id):
        """
        Update a user.

        Regular users may update only their own first and last names.
        Administrators may update any user's permitted fields.
        """

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        admin = claims.get("is_admin", False)

        if not admin and current_user_id != user_id:
            return {
                "error": "Unauthorized action"
            }, 403

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        user_data = api.payload.copy()

        if admin:
            valid, error = validate_admin_update(user_data)
        else:
            valid, error = validate_regular_update(user_data)

        if not valid:
            return {
                "error": error
            }, 400

        if "email" in user_data:
            new_email = user_data["email"].strip()

            existing_user = facade.get_user_by_email(new_email)

            if existing_user and existing_user.id != user_id:
                return {
                    "error": "Email already registered"
                }, 400

            user_data["email"] = new_email

        if "first_name" in user_data:
            user_data["first_name"] = user_data[
                "first_name"
            ].strip()

        if "last_name" in user_data:
            user_data["last_name"] = user_data[
                "last_name"
            ].strip()

        new_password = user_data.pop("password", None)

        updated_user = facade.update_user(
            user_id,
            user_data
        )

        if new_password:
            updated_user.hash_password(new_password)

        return serialize_user(updated_user), 200

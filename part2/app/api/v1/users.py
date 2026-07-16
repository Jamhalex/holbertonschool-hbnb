#!/usr/bin/python3
"""
User API endpoints.
"""

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
            description="Email address of the user"
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
        )
    }
)


def serialize_user(user):
    """
    Return a public dictionary representation of a user.
    """

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


def validate_user_data(user_data, require_all=True):
    """
    Validate user creation or update data.

    Args:
        user_data (dict): User data to validate.
        require_all (bool): Whether every user field is required.

    Returns:
        tuple: Validation result and optional error message.
    """

    allowed_fields = {
        "first_name",
        "last_name",
        "email"
    }

    if not user_data:
        return False, "No user data provided"

    if not set(user_data).issubset(allowed_fields):
        return False, "Invalid user field"

    required_fields = {
        "first_name",
        "last_name",
        "email"
    }

    if require_all and not required_fields.issubset(user_data):
        return False, "Missing required user data"

    if "first_name" in user_data:
        first_name = user_data["first_name"]

        if not isinstance(first_name, str) or not first_name.strip():
            return False, "First name is required"

    if "last_name" in user_data:
        last_name = user_data["last_name"]

        if not isinstance(last_name, str) or not last_name.strip():
            return False, "Last name is required"

    if "email" in user_data:
        email = user_data["email"]

        if not isinstance(email, str) or not email.strip():
            return False, "Email is required"

        if "@" not in email:
            return False, "Invalid email format"

    return True, None


def clean_user_data(user_data):
    """
    Trim whitespace from user string values.
    """

    cleaned_data = user_data.copy()

    for field in ("first_name", "last_name", "email"):
        if field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip()

    return cleaned_data


@api.route("/")
class UserList(Resource):
    """
    Handle user collection operations.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """
        Create a new user.
        """

        user_data = api.payload.copy()

        valid, error = validate_user_data(
            user_data,
            require_all=True
        )

        if not valid:
            return {
                "error": error
            }, 400

        user_data = clean_user_data(user_data)

        existing_user = facade.get_user_by_email(
            user_data["email"]
        )

        if existing_user:
            return {
                "error": "Email already registered"
            }, 400

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

    @api.response(200, "User retrieved successfully")
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

    @api.expect(update_user_model, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "User not found")
    def put(self, user_id):
        """
        Update a user.
        """

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        user_data = api.payload.copy()

        valid, error = validate_user_data(
            user_data,
            require_all=False
        )

        if not valid:
            return {
                "error": error
            }, 400

        user_data = clean_user_data(user_data)

        if "email" in user_data:
            existing_user = facade.get_user_by_email(
                user_data["email"]
            )

            if (
                existing_user
                and existing_user.id != user_id
            ):
                return {
                    "error": "Email already registered"
                }, 400

        updated_user = facade.update_user(
            user_id,
            user_data
        )

        return serialize_user(updated_user), 200

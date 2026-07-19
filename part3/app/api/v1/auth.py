#!/usr/bin/python3
"""
Authentication API endpoints.
"""

from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace(
    "auth",
    description="Authentication operations"
)


login_model = api.model(
    "Login",
    {
        "email": fields.String(
            required=True,
            description="User email"
        ),
        "password": fields.String(
            required=True,
            description="User password"
        )
    }
)


def validate_credentials(credentials):
    """
    Validate login credentials.

    Args:
        credentials (dict): Login request data.

    Returns:
        tuple: Validation result and optional error message.
    """

    if not credentials:
        return False, "Email and password are required"

    email = credentials.get("email")
    password = credentials.get("password")

    if not isinstance(email, str) or not email.strip():
        return False, "Email is required"

    if not isinstance(password, str) or not password:
        return False, "Password is required"

    return True, None


@api.route("/login")
class Login(Resource):
    """
    Handle user authentication.
    """

    @api.expect(login_model, validate=True)
    @api.response(200, "Login successful")
    @api.response(400, "Invalid input data")
    @api.response(401, "Invalid credentials")
    def post(self):
        """
        Authenticate a user and return a JWT access token.
        """

        credentials = api.payload.copy()

        valid, error = validate_credentials(credentials)

        if not valid:
            return {
                "error": error
            }, 400

        email = credentials["email"].strip().lower()
        password = credentials["password"]

        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            return {
                "error": "Invalid credentials"
            }, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "is_admin": bool(user.is_admin)
            }
        )

        return {
            "access_token": access_token
        }, 200

#!/usr/bin/python3
"""
HBnB Flask application initialization.

Creates and configures the Flask application using the
Application Factory pattern.
"""

from flask import Flask
from flask_restx import Api

from app.extensions import bcrypt, jwt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application.

    Args:
        config_class (str or object): Configuration class to load.

    Returns:
        Flask: Configured Flask application.
    """

    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(config_class)

    # Initialize Flask extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize REST API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    # Register API namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    return app

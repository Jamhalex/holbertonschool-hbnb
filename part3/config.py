#!/usr/bin/python3
"""
Application configuration classes.
"""

import os


class Config:
    """
    Base application configuration.
    """

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key-change-this-value"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret-key-change-this-value"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Development configuration using SQLite.
    """

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///development.db"
    )


class TestingConfig(Config):
    """
    Testing configuration using an in-memory SQLite database.
    """

    TESTING = True

    SECRET_KEY = (
        "testing-secret-key-with-at-least-thirty-two-bytes"
    )

    JWT_SECRET_KEY = (
        "testing-jwt-secret-key-with-at-least-thirty-two-bytes"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

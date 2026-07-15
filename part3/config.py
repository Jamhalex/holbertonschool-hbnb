#!/usr/bin/python3
"""
Application configuration.
"""

import os


class Config:
    """
    Base configuration.
    """

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_secret_key"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration.
    """

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///development.db"
    )


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}

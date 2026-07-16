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
        "default_secret_key"
    )
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration.
    """

    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}

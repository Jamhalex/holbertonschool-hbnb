#!/usr/bin/python3
"""
API authentication and authorization helpers.
"""

from flask_jwt_extended import get_jwt


def is_admin():
    """
    Return whether the authenticated user has administrator privileges.
    """

    claims = get_jwt()

    return claims.get("is_admin", False)

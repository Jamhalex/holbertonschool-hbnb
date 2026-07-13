#!/usr/bin/python3
"""
JWT authentication tests.
"""

import unittest

from app import create_app
from app.services import facade


class AuthTestCase(unittest.TestCase):
    """
    Tests JWT login behavior.
    """

    def setUp(self):
        """
        Create a fresh test application and client.
        """

        self.app = create_app("config.DevelopmentConfig")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()

        self.user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "password": "secret123"
        })

    def test_login_returns_access_token(self):
        """
        Valid credentials should return a JWT.
        """

        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@test.com",
                "password": "secret123"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())

    def test_login_rejects_wrong_password(self):
        """
        Invalid credentials should return 401.
        """

        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@test.com",
                "password": "wrong"
            }
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json(),
            {"error": "Invalid credentials"}
        )


if __name__ == "__main__":
    unittest.main()

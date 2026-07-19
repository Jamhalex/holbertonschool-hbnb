#!/usr/bin/python3
"""
Authentication tests for the HBnB API.
"""

import unittest

from flask_jwt_extended import decode_token

from app import create_app
from app.extensions import db
from app.services import facade


class AuthTestCase(unittest.TestCase):
    """
    Test JWT authentication behavior.
    """

    def setUp(self):
        """
        Create a fresh in-memory database and test client.
        """

        self.app = create_app("config.TestingConfig")
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        self.client = self.app.test_client()

        self.user = facade.create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": "user@test.com",
            "password": "password123",
            "is_admin": False
        })

        self.admin = facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "password": "admin123",
            "is_admin": True
        })

    def tearDown(self):
        """
        Remove database data after each test.
        """

        db.session.remove()
        db.drop_all()
        self.context.pop()

    def login(self, email, password):
        """
        Submit login credentials.

        Args:
            email (str): User email.
            password (str): Plain-text password.

        Returns:
            Flask response: Login endpoint response.
        """

        return self.client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

    def test_login_returns_access_token(self):
        """
        Test successful login returns a JWT access token.
        """

        response = self.login(
            "user@test.com",
            "password123"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("access_token", data)
        self.assertIsInstance(data["access_token"], str)
        self.assertTrue(data["access_token"])

    def test_regular_user_token_contains_correct_claims(self):
        """
        Test JWT identity and regular-user administrator claim.
        """

        response = self.login(
            "user@test.com",
            "password123"
        )

        token = response.get_json()["access_token"]
        decoded = decode_token(token)

        self.assertEqual(
            decoded["sub"],
            self.user.id
        )

        self.assertIn("is_admin", decoded)
        self.assertFalse(decoded["is_admin"])

    def test_admin_token_contains_admin_claim(self):
        """
        Test administrator JWT contains is_admin set to True.
        """

        response = self.login(
            "admin@test.com",
            "admin123"
        )

        token = response.get_json()["access_token"]
        decoded = decode_token(token)

        self.assertEqual(
            decoded["sub"],
            self.admin.id
        )

        self.assertTrue(decoded["is_admin"])

    def test_login_rejects_wrong_password(self):
        """
        Test login fails with an incorrect password.
        """

        response = self.login(
            "user@test.com",
            "wrong-password"
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "Invalid credentials"
        )

    def test_login_rejects_unknown_email(self):
        """
        Test login fails when the email does not exist.
        """

        response = self.login(
            "missing@test.com",
            "password123"
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "Invalid credentials"
        )

    def test_login_normalizes_email(self):
        """
        Test login accepts surrounding whitespace and uppercase email.
        """

        response = self.login(
            "  USER@TEST.COM  ",
            "password123"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "access_token",
            response.get_json()
        )

    def test_login_rejects_empty_email(self):
        """
        Test login rejects an empty email.
        """

        response = self.login(
            "",
            "password123"
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.get_json()["error"],
            "Email is required"
        )

    def test_login_rejects_empty_password(self):
        """
        Test login rejects an empty password.
        """

        response = self.login(
            "user@test.com",
            ""
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.get_json()["error"],
            "Password is required"
        )

    def test_password_is_hashed(self):
        """
        Test that plain-text passwords are not stored.
        """

        self.assertNotEqual(
            self.user.password,
            "password123"
        )

        self.assertTrue(
            self.user.password.startswith("$2")
        )

    def test_password_verification(self):
        """
        Test password verification behavior.
        """

        self.assertTrue(
            self.user.verify_password("password123")
        )

        self.assertFalse(
            self.user.verify_password("incorrect")
        )

    def test_user_serialization_excludes_password(self):
        """
        Test serialized user data never exposes the password.
        """

        user_data = self.user.to_dict()

        self.assertNotIn("password", user_data)
        self.assertEqual(
            user_data["email"],
            "user@test.com"
        )


if __name__ == "__main__":
    unittest.main()

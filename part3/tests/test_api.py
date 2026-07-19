#!/usr/bin/python3
"""
Tests for the authenticated HBnB API endpoints.
"""

import unittest

from app import create_app
from app.extensions import db
from app.services import facade


class HBnBApiTestCase(unittest.TestCase):
    """
    Test the HBnB REST API with SQLAlchemy and JWT.
    """

    def setUp(self):
        """
        Create a fresh in-memory database for each test.
        """

        self.app = create_app("config.TestingConfig")
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """
        Remove all database data after each test.
        """

        db.session.remove()
        db.drop_all()
        self.context.pop()

    def create_user(
        self,
        email="user@test.com",
        password="password123",
        is_admin=False
    ):
        """
        Create a user directly through the facade.
        """

        return facade.create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": password,
            "is_admin": is_admin
        })

    def login(self, email, password):
        """
        Log in and return a JWT access token.
        """

        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        self.assertEqual(response.status_code, 200)

        return response.get_json()["access_token"]

    def auth_headers(self, token):
        """
        Return an Authorization header.
        """

        return {
            "Authorization": f"Bearer {token}"
        }

    def create_admin_token(self):
        """
        Create an administrator and return its token.
        """

        self.create_user(
            email="admin@test.com",
            password="admin123",
            is_admin=True
        )

        return self.login(
            "admin@test.com",
            "admin123"
        )

    def create_regular_token(self):
        """
        Create a regular user and return the user and token.
        """

        user = self.create_user(
            email="regular@test.com",
            password="regular123"
        )

        token = self.login(
            "regular@test.com",
            "regular123"
        )

        return user, token

    # User tests

    def test_admin_can_create_user(self):
        """
        Test that an administrator can create a user.
        """

        token = self.create_admin_token()

        response = self.client.post(
            "/api/v1/users/",
            headers=self.auth_headers(token),
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@test.com",
                "password": "secret123",
                "is_admin": False
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["email"], "john@test.com")
        self.assertNotIn("password", data)

    def test_regular_user_cannot_create_user(self):
        """
        Test that a regular user cannot create another user.
        """

        _, token = self.create_regular_token()

        response = self.client.post(
            "/api/v1/users/",
            headers=self.auth_headers(token),
            json={
                "first_name": "Other",
                "last_name": "User",
                "email": "other@test.com",
                "password": "secret123"
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_create_user_requires_authentication(self):
        """
        Test that user creation requires a JWT.
        """

        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@test.com",
                "password": "secret123"
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_can_update_own_name(self):
        """
        Test that a user can update their own name.
        """

        user, token = self.create_regular_token()

        response = self.client.put(
            f"/api/v1/users/{user.id}",
            headers=self.auth_headers(token),
            json={
                "first_name": "Updated"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["first_name"],
            "Updated"
        )

    def test_regular_user_cannot_update_email(self):
        """
        Test that regular users cannot update their email.
        """

        user, token = self.create_regular_token()

        response = self.client.put(
            f"/api/v1/users/{user.id}",
            headers=self.auth_headers(token),
            json={
                "email": "changed@test.com"
            }
        )

        self.assertEqual(response.status_code, 400)

    # Amenity tests

    def test_admin_can_create_amenity(self):
        """
        Test that an administrator can create an amenity.
        """

        token = self.create_admin_token()

        response = self.client.post(
            "/api/v1/amenities/",
            headers=self.auth_headers(token),
            json={
                "name": "WiFi"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json()["name"],
            "WiFi"
        )

    def test_regular_user_cannot_create_amenity(self):
        """
        Test that regular users cannot create amenities.
        """

        _, token = self.create_regular_token()

        response = self.client.post(
            "/api/v1/amenities/",
            headers=self.auth_headers(token),
            json={
                "name": "Pool"
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_create_amenity_requires_authentication(self):
        """
        Test that amenity creation requires a JWT.
        """

        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "WiFi"
            }
        )

        self.assertEqual(response.status_code, 401)

    # Place tests

    def test_authenticated_user_can_create_place(self):
        """
        Test place creation by an authenticated user.
        """

        user, token = self.create_regular_token()

        response = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(token),
            json={
                "title": "Beach House",
                "description": "Ocean view",
                "price": 100,
                "latitude": 18.4,
                "longitude": -66.1,
                "amenity_ids": []
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["owner_id"], user.id)
        self.assertEqual(data["title"], "Beach House")

    def test_create_place_requires_authentication(self):
        """
        Test that place creation requires a JWT.
        """

        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Beach House",
                "description": "Ocean view",
                "price": 100,
                "latitude": 18.4,
                "longitude": -66.1
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_place_owner_can_update_place(self):
        """
        Test that a place owner can update their place.
        """

        _, token = self.create_regular_token()

        created = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(token),
            json={
                "title": "Cabin",
                "description": "Quiet cabin",
                "price": 120,
                "latitude": 18.2,
                "longitude": -66.4
            }
        )

        place_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/places/{place_id}",
            headers=self.auth_headers(token),
            json={
                "price": 150
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["price"],
            150
        )

    def test_non_owner_cannot_update_place(self):
        """
        Test that another regular user cannot update a place.
        """

        _, owner_token = self.create_regular_token()

        created = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(owner_token),
            json={
                "title": "Cabin",
                "description": "Quiet cabin",
                "price": 120,
                "latitude": 18.2,
                "longitude": -66.4
            }
        )

        place_id = created.get_json()["id"]

        self.create_user(
            email="other@test.com",
            password="other123"
        )

        other_token = self.login(
            "other@test.com",
            "other123"
        )

        response = self.client.put(
            f"/api/v1/places/{place_id}",
            headers=self.auth_headers(other_token),
            json={
                "price": 200
            }
        )

        self.assertEqual(response.status_code, 403)

    # Review tests

    def test_authenticated_user_can_create_review(self):
        """
        Test review creation by an authenticated user.
        """

        _, owner_token = self.create_regular_token()

        place_response = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(owner_token),
            json={
                "title": "Apartment",
                "description": "City apartment",
                "price": 90,
                "latitude": 18.3,
                "longitude": -66.0
            }
        )

        place_id = place_response.get_json()["id"]

        self.create_user(
            email="reviewer@test.com",
            password="review123"
        )

        reviewer_token = self.login(
            "reviewer@test.com",
            "review123"
        )

        response = self.client.post(
            "/api/v1/reviews/",
            headers=self.auth_headers(reviewer_token),
            json={
                "text": "Great place",
                "place_id": place_id
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["text"], "Great place")
        self.assertIn("user", data)

    def test_create_review_requires_authentication(self):
        """
        Test that review creation requires a JWT.
        """

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place",
                "place_id": "fake-place"
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_review_author_can_update_review(self):
        """
        Test that the review author can update a review.
        """

        _, owner_token = self.create_regular_token()

        place_response = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(owner_token),
            json={
                "title": "Apartment",
                "description": "City apartment",
                "price": 90,
                "latitude": 18.3,
                "longitude": -66.0
            }
        )

        place_id = place_response.get_json()["id"]

        self.create_user(
            email="reviewer@test.com",
            password="review123"
        )

        reviewer_token = self.login(
            "reviewer@test.com",
            "review123"
        )

        created = self.client.post(
            "/api/v1/reviews/",
            headers=self.auth_headers(reviewer_token),
            json={
                "text": "Good",
                "place_id": place_id
            }
        )

        review_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            headers=self.auth_headers(reviewer_token),
            json={
                "text": "Excellent"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["text"],
            "Excellent"
        )

    def test_duplicate_review_is_rejected(self):
        """
        Test that one user cannot review one place twice.
        """

        _, token = self.create_regular_token()

        place_response = self.client.post(
            "/api/v1/places/",
            headers=self.auth_headers(token),
            json={
                "title": "House",
                "description": "Test house",
                "price": 100,
                "latitude": 18.2,
                "longitude": -66.2
            }
        )

        place_id = place_response.get_json()["id"]

        review_data = {
            "text": "First review",
            "place_id": place_id
        }

        first = self.client.post(
            "/api/v1/reviews/",
            headers=self.auth_headers(token),
            json=review_data
        )

        second = self.client.post(
            "/api/v1/reviews/",
            headers=self.auth_headers(token),
            json=review_data
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)


if __name__ == "__main__":
    unittest.main()

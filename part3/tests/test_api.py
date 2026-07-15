#!/usr/bin/python3
"""
HBnB API endpoint tests.

Tests:
- User endpoints
- Amenity endpoints
- Place endpoints
- Review endpoints
- Validation responses
"""

import unittest

from app import create_app


class HBnBApiTestCase(unittest.TestCase):
    """
    Test cases for HBnB REST API.
    """

    def setUp(self):
        """
        Initialize Flask test client.
        """

        self.app = create_app()
        self.app.testing = True

        self.client = self.app.test_client()

        self.user_id = None
        self.amenity_id = None
        self.place_id = None
        self.review_id = None


    # ==========================
    # USER TESTS
    # ==========================

    def test_create_user(self):

        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@test.com",
                "password": "123456"
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )

        data = response.get_json()

        self.assertIn(
            "id",
            data
        )

        self.user_id = data["id"]



    def test_get_users(self):

        response = self.client.get(
            "/api/v1/users/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIsInstance(
            response.get_json(),
            list
        )



    def test_invalid_user_payload(self):

        response = self.client.post(
            "/api/v1/users/",
            json={}
        )

        self.assertEqual(
            response.status_code,
            400
        )


    # ==========================
    # AMENITY TESTS
    # ==========================

    def test_create_amenity(self):

        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "WiFi"
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )


        data = response.get_json()

        self.assertIn(
            "id",
            data
        )

        self.amenity_id = data["id"]



    def test_get_amenities(self):

        response = self.client.get(
            "/api/v1/amenities/"
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_empty_amenity_name(self):

        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": ""
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )


    # ==========================
    # PLACE TESTS
    # ==========================

    def test_create_place(self):

        user = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Owner",
                "last_name": "User",
                "email": "owner@test.com",
                "password": "123456"
            }
        )

        user_id = user.get_json()["id"]


        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Beach House",
                "description": "Ocean view",
                "price": 100,
                "latitude": 40.0,
                "longitude": -70.0,
                "owner_id": user_id
            }
        )


        self.assertEqual(
            response.status_code,
            201
        )


        data = response.get_json()

        self.assertIn(
            "id",
            data
        )

        self.place_id = data["id"]



    def test_invalid_price(self):

        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Bad House",
                "description": "Bad",
                "price": -10,
                "latitude": 40,
                "longitude": -70,
                "owner_id": "fake"
            }
        )


        self.assertEqual(
            response.status_code,
            400
        )



    # ==========================
    # REVIEW TESTS
    # ==========================

    def test_create_review(self):

        user = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Review",
                "last_name": "User",
                "email": "review@test.com",
                "password": "123456"
            }
        )

        user_id = user.get_json()["id"]


        place = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Apartment",
                "description": "Nice",
                "price": 80,
                "latitude": 40,
                "longitude": -70,
                "owner_id": user_id
            }
        )

        place_id = place.get_json()["id"]


        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place",
                "user_id": user_id,
                "place_id": place_id
            }
        )


        self.assertEqual(
            response.status_code,
            201
        )


    def test_empty_review_text(self):

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "",
                "user_id": "fake",
                "place_id": "fake"
            }
        )


        self.assertEqual(
            response.status_code,
            400
        )



if __name__ == "__main__":

    unittest.main()

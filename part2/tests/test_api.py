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
from app.services import facade


class HBnBApiTestCase(unittest.TestCase):
    """
    Test cases for the HBnB REST API.
    """

    def setUp(self):
        """
        Initialize a clean Flask test client.
        """

        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()

    def create_user(
        self,
        first_name="John",
        last_name="Doe",
        email="john@test.com"
    ):
        """
        Create and return a test user response.
        """

        return self.client.post(
            "/api/v1/users/",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        )

    def create_place(self, owner_id):
        """
        Create and return a test place response.
        """

        return self.client.post(
            "/api/v1/places/",
            json={
                "title": "Beach House",
                "description": "Ocean view",
                "price": 100,
                "latitude": 40.0,
                "longitude": -70.0,
                "owner_id": owner_id
            }
        )

    # User tests

    def test_create_user(self):
        """
        Test successful user creation.
        """

        response = self.create_user()

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john@test.com")

    def test_get_users(self):
        """
        Test retrieving all users.
        """

        self.create_user()

        response = self.client.get(
            "/api/v1/users/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_user_by_id(self):
        """
        Test retrieving a user by ID.
        """

        created = self.create_user()
        user_id = created.get_json()["id"]

        response = self.client.get(
            f"/api/v1/users/{user_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["email"],
            "john@test.com"
        )

    def test_update_user(self):
        """
        Test updating a user.
        """

        created = self.create_user()
        user_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/users/{user_id}",
            json={
                "first_name": "Jane"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["first_name"],
            "Jane"
        )

    def test_duplicate_user_email(self):
        """
        Test rejection of duplicate email addresses.
        """

        self.create_user()

        response = self.create_user(
            first_name="Other",
            last_name="User",
            email="john@test.com"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_user_payload(self):
        """
        Test rejection of an empty user payload.
        """

        response = self.client.post(
            "/api/v1/users/",
            json={}
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_user_email(self):
        """
        Test rejection of an invalid email address.
        """

        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "invalid-email"
            }
        )

        self.assertEqual(response.status_code, 400)

    # Amenity tests

    def test_create_amenity(self):
        """
        Test successful amenity creation.
        """

        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "WiFi"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_get_amenities(self):
        """
        Test retrieving all amenities.
        """

        self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "WiFi"
            }
        )

        response = self.client.get(
            "/api/v1/amenities/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_update_amenity(self):
        """
        Test updating an amenity.
        """

        created = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": "WiFi"
            }
        )

        amenity_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            json={
                "name": "Wireless Internet"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["name"],
            "Wireless Internet"
        )

    def test_empty_amenity_name(self):
        """
        Test rejection of an empty amenity name.
        """

        response = self.client.post(
            "/api/v1/amenities/",
            json={
                "name": ""
            }
        )

        self.assertEqual(response.status_code, 400)

    # Place tests

    def test_create_place(self):
        """
        Test successful place creation.
        """

        user = self.create_user(
            first_name="Owner",
            last_name="User",
            email="owner@test.com"
        )

        user_id = user.get_json()["id"]

        response = self.create_place(user_id)

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["owner_id"], user_id)

    def test_get_places(self):
        """
        Test retrieving all places.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        self.create_place(user_id)

        response = self.client.get(
            "/api/v1/places/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_place_by_id(self):
        """
        Test retrieving a place by ID.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        created = self.create_place(user_id)
        place_id = created.get_json()["id"]

        response = self.client.get(
            f"/api/v1/places/{place_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["title"],
            "Beach House"
        )

    def test_update_place(self):
        """
        Test updating a place.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        created = self.create_place(user_id)
        place_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/places/{place_id}",
            json={
                "price": 150
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["price"],
            150
        )

    def test_invalid_price(self):
        """
        Test rejection of a non-positive price.
        """

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

        self.assertEqual(response.status_code, 400)

    def test_invalid_latitude(self):
        """
        Test rejection of an invalid latitude.
        """

        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Bad House",
                "description": "Bad",
                "price": 10,
                "latitude": 100,
                "longitude": -70,
                "owner_id": "fake"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_owner_not_found(self):
        """
        Test place creation with a nonexistent owner.
        """

        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "House",
                "description": "Description",
                "price": 100,
                "latitude": 40,
                "longitude": -70,
                "owner_id": "missing-owner"
            }
        )

        self.assertEqual(response.status_code, 404)

    # Review tests

    def test_create_review(self):
        """
        Test successful review creation.
        """

        user = self.create_user(
            first_name="Review",
            last_name="User",
            email="review@test.com"
        )

        user_id = user.get_json()["id"]

        place = self.create_place(user_id)
        place_id = place.get_json()["id"]

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place",
                "user_id": user_id,
                "place_id": place_id
            }
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["text"], "Great place")
        self.assertEqual(data["user_id"], user_id)
        self.assertEqual(data["place_id"], place_id)

    def test_get_reviews(self):
        """
        Test retrieving all reviews.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        place = self.create_place(user_id)
        place_id = place.get_json()["id"]

        self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place",
                "user_id": user_id,
                "place_id": place_id
            }
        )

        response = self.client.get(
            "/api/v1/reviews/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_update_review(self):
        """
        Test updating review text.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        place = self.create_place(user_id)
        place_id = place.get_json()["id"]

        created = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Good",
                "user_id": user_id,
                "place_id": place_id
            }
        )

        review_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={
                "text": "Excellent"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["text"],
            "Excellent"
        )

    def test_delete_review(self):
        """
        Test deleting a review.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        place = self.create_place(user_id)
        place_id = place.get_json()["id"]

        created = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Good",
                "user_id": user_id,
                "place_id": place_id
            }
        )

        review_id = created.get_json()["id"]

        response = self.client.delete(
            f"/api/v1/reviews/{review_id}"
        )

        self.assertEqual(response.status_code, 200)

        missing = self.client.get(
            f"/api/v1/reviews/{review_id}"
        )

        self.assertEqual(missing.status_code, 404)

    def test_get_reviews_by_place(self):
        """
        Test retrieving reviews for a specific place.
        """

        user = self.create_user()
        user_id = user.get_json()["id"]

        place = self.create_place(user_id)
        place_id = place.get_json()["id"]

        self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place",
                "user_id": user_id,
                "place_id": place_id
            }
        )

        response = self.client.get(
            f"/api/v1/reviews/places/{place_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_empty_review_text(self):
        """
        Test rejection of an empty review.
        """

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "",
                "user_id": "fake",
                "place_id": "fake"
            }
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

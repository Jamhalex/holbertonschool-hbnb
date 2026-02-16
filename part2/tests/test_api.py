#!/usr/bin/python3
import unittest

from app import create_app


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()
        cls.facade = cls.app.config["FACADE"]

    def setUp(self):
        self.facade.repo.reset()

    def create_user(self, email="user@example.com"):
        payload = {
            "email": email,
            "first_name": "Test",
            "last_name": "User",
            "password": "secret",
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()["id"]

    def create_amenity(self, name="Wifi"):
        resp = self.client.post("/api/v1/amenities/", json={"name": name})
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()["id"]

    def create_place(self, owner_id, amenity_ids=None):
        if amenity_ids is None:
            amenity_ids = []
        payload = {
            "title": "Cozy Loft",
            "description": "Great place",
            "price": 120,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id,
            "amenity_ids": amenity_ids,
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()["id"]

    def create_review(self, user_id, place_id, text="Nice stay", rating=5):
        payload = {
            "text": text,
            "user_id": user_id,
            "place_id": place_id,
            "rating": rating,
        }
        resp = self.client.post("/api/v1/reviews/", json=payload)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()["id"]

    def test_user_flow(self):
        user_id = self.create_user()
        resp = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.put(f"/api/v1/users/{user_id}", json={"first_name": "Updated"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["first_name"], "Updated")

    def test_amenity_flow(self):
        amenity_id = self.create_amenity()
        resp = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.put(f"/api/v1/amenities/{amenity_id}", json={"name": "Pool"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Pool")

    def test_place_flow(self):
        owner_id = self.create_user()
        amenity_id = self.create_amenity()
        place_id = self.create_place(owner_id, [amenity_id])
        resp = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("owner", data)
        self.assertIn("amenities", data)
        resp = self.client.put(f"/api/v1/places/{place_id}", json={"price": 150})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["price"], 150.0)

    def test_review_flow(self):
        user_id = self.create_user()
        place_id = self.create_place(user_id)
        review_id = self.create_review(user_id, place_id)
        resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.put(f"/api/v1/reviews/{review_id}", json={"text": "Updated review"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["text"], "Updated review")
        resp = self.client.get("/api/v1/reviews/")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(f"/api/v1/places/{place_id}/reviews")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertIn(resp.status_code, (200, 204))

    def test_validation_user_missing_email(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password": "secret",
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_user_invalid_email_and_empty_first_name(self):
        payload = {
            "email": "bad-email",
            "first_name": "Test",
            "last_name": "User",
            "password": "secret",
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 400)

        payload = {
            "email": "valid@example.com",
            "first_name": "   ",
            "last_name": "User",
            "password": "secret",
        }
        resp = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_amenity_missing_name(self):
        resp = self.client.post("/api/v1/amenities/", json={})
        self.assertEqual(resp.status_code, 400)

    def test_validation_place_missing_title_or_owner(self):
        owner_id = self.create_user()
        payload = {
            "description": "Missing title",
            "price": 50,
            "latitude": 0,
            "longitude": 0,
            "owner_id": owner_id,
            "amenity_ids": [],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

        payload = {
            "title": "No owner",
            "description": "Missing owner_id",
            "price": 50,
            "latitude": 0,
            "longitude": 0,
            "amenity_ids": [],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_place_price_and_coords(self):
        owner_id = self.create_user()
        payload = {
            "title": "Bad price",
            "description": "price <= 0",
            "price": 0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": owner_id,
            "amenity_ids": [],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

        payload = {
            "title": "Bad lat",
            "description": "lat out of range",
            "price": 10,
            "latitude": 91,
            "longitude": 0,
            "owner_id": owner_id,
            "amenity_ids": [],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

        payload = {
            "title": "Bad lon",
            "description": "lon out of range",
            "price": 10,
            "latitude": 0,
            "longitude": 181,
            "owner_id": owner_id,
            "amenity_ids": [],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_place_amenity_ids_not_list(self):
        owner_id = self.create_user()
        payload = {
            "title": "Bad amenities",
            "description": "amenity_ids not list",
            "price": 50,
            "latitude": 0,
            "longitude": 0,
            "owner_id": owner_id,
            "amenity_ids": "not-a-list",
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_place_amenity_ids_not_string(self):
        owner_id = self.create_user()
        payload = {
            "title": "Bad amenity ids",
            "description": "amenity_ids not string",
            "price": 50,
            "latitude": 0,
            "longitude": 0,
            "owner_id": owner_id,
            "amenity_ids": [123],
        }
        resp = self.client.post("/api/v1/places/", json=payload)
        self.assertEqual(resp.status_code, 400)

    def test_validation_review_missing_fields(self):
        user_id = self.create_user()
        place_id = self.create_place(user_id)

        resp = self.client.post("/api/v1/reviews/", json={"user_id": user_id, "place_id": place_id})
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post("/api/v1/reviews/", json={"text": "Nice", "place_id": place_id})
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post("/api/v1/reviews/", json={"text": "Nice", "user_id": user_id})
        self.assertEqual(resp.status_code, 400)

    def test_validation_review_empty_text(self):
        user_id = self.create_user()
        place_id = self.create_place(user_id)
        resp = self.client.post(
            "/api/v1/reviews/",
            json={"text": "   ", "user_id": user_id, "place_id": place_id},
        )
        self.assertEqual(resp.status_code, 400)

    def test_validation_review_put_empty_text(self):
        user_id = self.create_user()
        place_id = self.create_place(user_id)
        review_id = self.create_review(user_id, place_id)
        resp = self.client.put(f"/api/v1/reviews/{review_id}", json={"text": ""})
        self.assertEqual(resp.status_code, 400)

    def test_validation_review_rating_invalid(self):
        user_id = self.create_user()
        place_id = self.create_place(user_id)
        resp = self.client.post(
            "/api/v1/reviews/",
            json={"text": "Nice", "user_id": user_id, "place_id": place_id, "rating": 6},
        )
        self.assertEqual(resp.status_code, 400)

    def test_not_found_cases(self):
        resp = self.client.get("/api/v1/users/bad-id")
        self.assertEqual(resp.status_code, 404)

        resp = self.client.put("/api/v1/places/bad-id", json={"title": "X"})
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get("/api/v1/places/bad-id/reviews")
        self.assertEqual(resp.status_code, 404)

        resp = self.client.delete("/api/v1/reviews/bad-id")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()

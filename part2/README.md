# HBnB — Part 2 (API)

## Run the server

From `part2/`:

```bash
python3 -m app.main
```

By default the API is available at `http://127.0.0.1:5000/api/v1`.

## Review endpoints (sanity curl examples)

Set IDs first (replace values with real IDs returned by the API):

```bash
BASE_URL="http://127.0.0.1:5000/api/v1"
USER_ID="<user-id>"
PLACE_ID="<place-id>"
```

Optional helper to create a user and place and capture IDs (no jq needed):

```bash
USER_ID=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test.user@example.com", "first_name": "Test", "last_name": "User", "password": "secret"}' \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')

PLACE_ID=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Place", "description": "Nice spot", "price": 100, "latitude": 37.77, "longitude": -122.42, "owner_id": "'"$USER_ID"'", "amenity_ids": []}' \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
```

Create a review:

```bash
curl -s -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great stay!", "user_id": "'"$USER_ID"'", "place_id": "'"$PLACE_ID"'"}'
```

List all reviews:

```bash
curl -s "$BASE_URL/reviews/"
```

Get a single review:

```bash
REVIEW_ID="<review-id>"
curl -s "$BASE_URL/reviews/$REVIEW_ID"
```

Update review text:

```bash
curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated review text"}'
```

Delete a review:

```bash
curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID"
```

List reviews by place:

```bash
curl -s "$BASE_URL/places/$PLACE_ID/reviews"
```

#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://127.0.0.1:5000/api/v1}

json_id() {
  python3 -c "import json,sys; print(json.load(sys.stdin)['id'])"
}

echo "== Create user =="
USER_JSON=$(curl -sS -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","first_name":"Alice","last_name":"Tester","password":"secret"}')
USER_ID=$(printf '%s' "$USER_JSON" | json_id)
printf 'User id: %s\n' "$USER_ID"

printf '\n== User failure (missing email) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" -d '{"first_name":"A","last_name":"B","password":"secret"}'

printf '\n== Create amenity ==\n'
AMENITY_JSON=$(curl -sS -X POST "$BASE_URL/amenities/" -H "Content-Type: application/json" \
  -d '{"name":"Wifi"}')
AMENITY_ID=$(printf '%s' "$AMENITY_JSON" | json_id)
printf 'Amenity id: %s\n' "$AMENITY_ID"

printf '\n== Amenity failure (missing name) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" -d '{}'

printf '\n== Create place ==\n'
PLACE_JSON=$(curl -sS -X POST "$BASE_URL/places/" -H "Content-Type: application/json" \
  -d "{\"title\":\"Cozy Loft\",\"description\":\"Great place\",\"price\":120,\"latitude\":37.7749,\"longitude\":-122.4194,\"owner_id\":\"$USER_ID\",\"amenity_ids\":[\"$AMENITY_ID\"]}")
PLACE_ID=$(printf '%s' "$PLACE_JSON" | json_id)
printf 'Place id: %s\n' "$PLACE_ID"

printf '\n== Place failure (missing owner_id) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"No owner","description":"x","price":10,"latitude":0,"longitude":0,"amenity_ids":[]}'

printf '\n== Place failure (not found reviews by bad place id) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X GET "$BASE_URL/places/bad-id/reviews"

printf '\n== Create review ==\n'
REVIEW_JSON=$(curl -sS -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" \
  -d "{\"text\":\"Nice stay\",\"user_id\":\"$USER_ID\",\"place_id\":\"$PLACE_ID\",\"rating\":5}")
REVIEW_ID=$(printf '%s' "$REVIEW_JSON" | json_id)
printf 'Review id: %s\n' "$REVIEW_ID"

printf '\n== Review failure (missing text) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"$USER_ID\",\"place_id\":\"$PLACE_ID\"}"

printf '\n== Delete review ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X DELETE "$BASE_URL/reviews/$REVIEW_ID"

printf '\n== Review failure (delete bad id) ==\n'
curl -sS -o /dev/null -w "Status: %{http_code}\n" -X DELETE "$BASE_URL/reviews/bad-id"

printf '\nDone.\n'

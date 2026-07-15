PRAGMA foreign_keys = ON;

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Test',
    'User',
    'test@example.com',
    'temporary-test-hash',
    FALSE
);

INSERT INTO places (
    id,
    title,
    description,
    price,
    latitude,
    longitude,
    owner_id
)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Test House',
    'Created by the CRUD test',
    125.00,
    18.4655,
    -66.1057,
    '11111111-1111-1111-1111-111111111111'
);

INSERT INTO reviews (
    id,
    text,
    user_id,
    place_id
)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    'Excellent property',
    '11111111-1111-1111-1111-111111111111',
    '22222222-2222-2222-2222-222222222222'
);

INSERT INTO place_amenity (
    place_id,
    amenity_id
)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    '550e8400-e29b-41d4-a716-446655440000'
);

SELECT
    places.title,
    users.email AS owner_email,
    reviews.text AS review,
    amenities.name AS amenity
FROM places
JOIN users
    ON users.id = places.owner_id
LEFT JOIN reviews
    ON reviews.place_id = places.id
LEFT JOIN place_amenity
    ON place_amenity.place_id = places.id
LEFT JOIN amenities
    ON amenities.id = place_amenity.amenity_id;

UPDATE places
SET
    price = 150.00,
    updated_at = CURRENT_TIMESTAMP
WHERE id = '22222222-2222-2222-2222-222222222222';

SELECT id, title, price
FROM places
WHERE id = '22222222-2222-2222-2222-222222222222';

DELETE FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';

SELECT COUNT(*) AS remaining_reviews
FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';

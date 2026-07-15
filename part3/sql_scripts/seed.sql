-- Initial HBnB administrator and amenities.

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
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$7hSkKPNaGfr4nYwCfAOtuOC3yapt7HKVvJnPqP5uIwLIurAX0wUYG',
    TRUE
);

INSERT INTO amenities (
    id,
    name
)
VALUES
(
    '550e8400-e29b-41d4-a716-446655440000',
    'WiFi'
),
(
    '550e8400-e29b-41d4-a716-446655440001',
    'Swimming Pool'
),
(
    '550e8400-e29b-41d4-a716-446655440002',
    'Air Conditioning'
);

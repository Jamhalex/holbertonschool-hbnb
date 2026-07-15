-- HBnB database schema for SQLite.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    latitude FLOAT NOT NULL
        CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT NOT NULL
        CHECK (longitude >= -180 AND longitude <= 180),
    owner_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    place_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE,
    FOREIGN KEY (amenity_id)
        REFERENCES amenities(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_places_owner_id
ON places(owner_id);

CREATE INDEX idx_reviews_user_id
ON reviews(user_id);

CREATE INDEX idx_reviews_place_id
ON reviews(place_id);

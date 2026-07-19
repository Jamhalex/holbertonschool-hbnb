#!/usr/bin/python3
"""
User model for the HBnB application.
"""

from app.extensions import bcrypt, db
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    SQLAlchemy model representing a user.
    """

    __tablename__ = "users"

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    places = db.relationship(
        "Place",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy=True
    )

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
        is_admin=False
    ):
        """
        Initialize a User instance.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            email (str): User's unique email address.
            password (str): Plain-text password to hash.
            is_admin (bool): Administrator status.
        """

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """
        Hash and store a plain-text password.

        Args:
            password (str): Plain-text password.

        Raises:
            ValueError: If the password is empty or invalid.
        """

        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password is required")

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """
        Verify a plain-text password against the stored hash.

        Args:
            password (str): Plain-text password to verify.

        Returns:
            bool: True if the password matches, otherwise False.
        """

        if (
            not self.password
            or not isinstance(password, str)
            or not password
        ):
            return False

        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def update(self, data):
        """
        Update user attributes safely.

        Password values are hashed before storage.
        """

        update_data = data.copy()
        new_password = update_data.pop("password", None)

        if "first_name" in update_data:
            update_data["first_name"] = update_data[
                "first_name"
            ].strip()

        if "last_name" in update_data:
            update_data["last_name"] = update_data[
                "last_name"
            ].strip()

        if "email" in update_data:
            update_data["email"] = update_data[
                "email"
            ].strip().lower()

        super().update(update_data)

        if new_password is not None:
            self.hash_password(new_password)

    def to_dict(self):
        """
        Return user data without exposing the password.
        """

        data = super().to_dict()

        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })

        return data

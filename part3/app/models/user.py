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
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    places = db.relationship(
        "Place",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        """
        Initialize a User instance.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """
        Hash and store the user's password.
        """

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """
        Verify a plain-text password against the stored hash.
        """

        if not self.password:
            return False

        return bcrypt.check_password_hash(
            self.password,
            password
        )

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

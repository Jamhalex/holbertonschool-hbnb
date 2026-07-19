#!/usr/bin/python3
"""
Base model class for all HBnB entities.
"""

from datetime import UTC, datetime
import uuid

from app.extensions import db


def utc_now():
    """
    Return the current timezone-aware UTC datetime.
    """

    return datetime.now(UTC)


class BaseModel(db.Model):
    """
    Abstract parent class for all SQLAlchemy models.
    """

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    def update(self, data):
        """
        Update model attributes except protected fields.
        """

        protected_fields = {
            "id",
            "created_at",
            "updated_at"
        }

        for key, value in data.items():
            if key in protected_fields:
                continue

            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = utc_now()

    def to_dict(self):
        """
        Return a dictionary representation of the object.
        """

        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

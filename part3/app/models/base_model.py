#!/usr/bin/python3
"""
Base model class for all HBnB entities.
"""

from datetime import datetime
import uuid

from app.extensions import db


class BaseModel(db.Model):
    """
    Parent class for all SQLAlchemy models.
    """

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def update(self, data):
        """
        Update object attributes.
        """

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Return a dictionary representation of the object.
        """

        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

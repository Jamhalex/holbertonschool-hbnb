#!/usr/bin/python3
"""
Repository interfaces and persistence implementations.
"""

from abc import ABC, abstractmethod

from app.extensions import db


class Repository(ABC):
    """
    Abstract repository interface.
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.
        """

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by ID.
        """

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects.
        """

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object.
        """

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object.
        """

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by an attribute.
        """


class InMemoryRepository(Repository):
    """
    Repository that stores objects in memory.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        """

        self._storage = {}

    def add(self, obj):
        """
        Add an object to memory.
        """

        self._storage[obj.id] = obj

        return obj

    def get(self, obj_id):
        """
        Retrieve an object by ID.
        """

        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all stored objects.
        """

        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object in memory.
        """

        obj = self.get(obj_id)

        if not obj:
            return None

        obj.update(data)

        return obj

    def delete(self, obj_id):
        """
        Delete an object from memory.
        """

        if obj_id not in self._storage:
            return False

        del self._storage[obj_id]

        return True

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve the first object matching an attribute.
        """

        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None
        )


class SQLAlchemyRepository(Repository):
    """
    Generic repository backed by SQLAlchemy.
    """

    def __init__(self, model):
        """
        Initialize the repository.

        Args:
            model: SQLAlchemy model class managed by the repository.
        """

        self.model = model

    def add(self, obj):
        """
        Add and persist an object.
        """

        db.session.add(obj)
        db.session.commit()

        return obj

    def get(self, obj_id):
        """
        Retrieve an object by primary key.
        """

        return db.session.get(
            self.model,
            obj_id
        )

    def get_all(self):
        """
        Retrieve all objects.
        """

        statement = db.select(self.model)

        return list(
            db.session.execute(
                statement
            ).scalars()
        )

    def update(self, obj_id, data):
        """
        Update and persist an existing object.
        """

        obj = self.get(obj_id)

        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()

        return obj

    def delete(self, obj_id):
        """
        Delete an object from the database.
        """

        obj = self.get(obj_id)

        if not obj:
            return False

        db.session.delete(obj)
        db.session.commit()

        return True

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve the first object matching an attribute.
        """

        if not hasattr(self.model, attr_name):
            return None

        statement = db.select(
            self.model
        ).filter_by(
            **{
                attr_name: attr_value
            }
        )

        return db.session.execute(
            statement
        ).scalar_one_or_none()

#!/usr/bin/python3
"""
Repository interface and in-memory implementation.
"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Define the common repository interface.
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
        Update an object using the supplied data.
        """

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object by ID.
        """

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by an attribute value.
        """


class InMemoryRepository(Repository):
    """
    Store and manage objects in memory.
    """

    def __init__(self):
        """
        Initialize empty in-memory storage.
        """

        self._storage = {}

    def add(self, obj):
        """
        Add an object to storage.

        Args:
            obj: Object to store.

        Returns:
            The stored object.
        """

        self._storage[obj.id] = obj

        return obj

    def get(self, obj_id):
        """
        Retrieve an object by ID.

        Args:
            obj_id (str): Object identifier.

        Returns:
            The matching object, or None.
        """

        return self._storage.get(obj_id)

    def get_all(self):
        """
        Return all stored objects.

        Returns:
            list: All objects in storage.
        """

        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update a stored object.

        Args:
            obj_id (str): Object identifier.
            data (dict): Attributes and values to update.

        Returns:
            The updated object, or None.
        """

        obj = self.get(obj_id)

        if not obj:
            return None

        obj.update(data)

        return obj

    def delete(self, obj_id):
        """
        Delete a stored object.

        Args:
            obj_id (str): Object identifier.

        Returns:
            bool: True if deleted, otherwise False.
        """

        if obj_id not in self._storage:
            return False

        del self._storage[obj_id]

        return True

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve the first object matching an attribute value.

        Args:
            attr_name (str): Attribute name.
            attr_value: Expected attribute value.

        Returns:
            The matching object, or None.
        """

        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None
        )

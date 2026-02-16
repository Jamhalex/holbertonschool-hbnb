#!/usr/bin/python3
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class ValidationError(Exception):
    pass


class InMemoryRepository:
    """
    Simple in-memory repository:
    storage = {"User": {"uuid": obj, ...}, ...}
    """

    def __init__(self) -> None:
        self._storage: Dict[str, Dict[str, Any]] = {}
        # Example uniqueness index: {"User.email": {"a@b.com": user_id}}
        self._unique: Dict[str, Dict[str, str]] = {}

    def reset(self) -> None:
        self._storage.clear()
        self._unique.clear()

    def _bucket(self, model_name: str) -> Dict[str, Any]:
        return self._storage.setdefault(model_name, {})

    def add(self, obj: Any) -> Any:
        model_name = obj.__class__.__name__
        bucket = self._bucket(model_name)

        # Validate if supported
        if hasattr(obj, "validate"):
            try:
                obj.validate()
            except (TypeError, ValueError) as e:
                raise ValidationError(str(e)) from e

        # Unique constraint: User.email
        if model_name == "User":
            email = getattr(obj, "email", "")
            if isinstance(email, str):
                key = "User.email"
                index = self._unique.setdefault(key, {})
                if email in index:
                    raise ConflictError("email already exists")
                index[email] = obj.id

        bucket[obj.id] = obj
        return obj

    def get(self, model_cls: Type[Any], obj_id: str) -> Any:
        model_name = model_cls.__name__
        bucket = self._bucket(model_name)
        obj = bucket.get(obj_id)
        if obj is None:
            raise NotFoundError(f"{model_name} not found")
        return obj

    def all(self, model_cls: Type[Any]) -> List[Any]:
        model_name = model_cls.__name__
        return list(self._bucket(model_name).values())

    def update(self, obj: Any, updates: Dict[str, Any]) -> Any:
        # Validate existence
        model_name = obj.__class__.__name__
        bucket = self._bucket(model_name)
        if obj.id not in bucket:
            raise NotFoundError(f"{model_name} not found")

        # Unique constraint update (User.email)
        if model_name == "User" and "email" in updates:
            new_email = updates.get("email")
            if not isinstance(new_email, str) or not new_email.strip():
                raise ValidationError("email is required")

            key = "User.email"
            index = self._unique.setdefault(key, {})
            current_email = getattr(obj, "email", "")
            if new_email != current_email:
                if new_email in index:
                    raise ConflictError("email already exists")
                # move index
                if isinstance(current_email, str) and current_email in index:
                    del index[current_email]
                index[new_email] = obj.id

        # Apply updates (simple attributes only)
        for k, v in updates.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

        # Validate after update
        if hasattr(obj, "validate"):
            try:
                obj.validate()
            except (TypeError, ValueError) as e:
                raise ValidationError(str(e)) from e

        if hasattr(obj, "touch"):
            obj.touch()

        return obj

    def delete(self, model_cls: Type[Any], obj_id: str) -> None:
        model_name = model_cls.__name__
        bucket = self._bucket(model_name)
        obj = bucket.pop(obj_id, None)
        if obj is None:
            raise NotFoundError(f"{model_name} not found")

        # Clean unique index
        if model_name == "User":
            email = getattr(obj, "email", "")
            key = "User.email"
            index = self._unique.setdefault(key, {})
            if isinstance(email, str) and email in index:
                del index[email]
   

    def exists(self, model_cls, obj_id: str) -> bool:
        model_name = model_cls.__name__
        return obj_id in self._bucket(model_name)

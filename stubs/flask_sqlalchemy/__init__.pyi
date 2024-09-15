"""__init__.pyi"""
from __future__ import annotations
from typing import Any, TypeVar, Generic, Type
from sqlalchemy.orm import Session

_T = TypeVar("_T", bound="Model")


class Model:
    query: Any


class SQLAlchemy:
    Model: Type[Model]
    session: ScopedSession

    def __init__(self, app: Any = ...) -> None:
        ...

    def init_app(self, app: Any) -> None:
        ...

    def create_all(self) -> None:
        ...

    def drop_all(self) -> None:
        ...


class ScopedSession:

    def __init__(self, session_factory: Any) -> None:
        ...

    def remove(self) -> None:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> Session:
        ...

    def add(self, instance: Any) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def close(self) -> None:
        ...

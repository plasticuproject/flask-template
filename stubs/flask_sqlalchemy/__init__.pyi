"""__init__.pyi"""
from __future__ import annotations
from typing import Any, TypeVar, Generic, Type
from sqlalchemy.orm import Session

_T = TypeVar('_T', bound='Model')


class Model:
    query: Any


class SQLAlchemy:
    Model: Type[Model]
    session: Session

    def __init__(self, app: Any = ...) -> None:
        ...

    def init_app(self, app: Any) -> None:
        ...

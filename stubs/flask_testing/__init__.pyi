"""__init__.pyi"""
from __future__ import annotations
from typing import Generic, Any, TypeVar

T = TypeVar("T")


class FlaskClient(Generic[T]):

    def post(self, path: str, data: dict[str, Any], **kwargs: Any) -> T:
        ...

    def get(self, path: str, **kwargs: Any) -> T:
        ...

    def test_client(self) -> FlaskClient[T]:
        ...  # Returns a FlaskClient


class FlaskCliRunner:

    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        ...

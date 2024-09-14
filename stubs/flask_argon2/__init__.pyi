"""__init__.pyi"""
from __future__ import annotations
from typing import Any


class Argon2:

    def __init__(self, app: Any = ...) -> None:
        ...

    def init_app(self, app: Any) -> None:
        ...

    def generate_password_hash(self, password: str, **kwargs: Any) -> str:
        ...

    def check_password_hash(self, pw_hash: str, password: str) -> bool:
        ...

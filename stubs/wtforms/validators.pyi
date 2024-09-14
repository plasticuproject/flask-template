"""validators.pyi"""
from __future__ import annotations
from typing import Any


class DataRequired:

    def __init__(self, message: str = ...) -> None:
        ...

    def __call__(self, form: Any, field: Any) -> None:
        ...


class Length:

    def __init__(self, min: int = 0, max: int = ...) -> None:
        ...

    def __call__(self, form: Any, field: Any) -> None:
        ...


class EqualTo:

    def __init__(self, fieldname: str, message: str = ...) -> None:
        ...

    def __call__(self, form: Any, field: Any) -> None:
        ...


class Regexp:

    def __init__(self, regex: str, flags: int = 0, message: str = ...) -> None:
        ...

    def __call__(self, form: Any, field: Any) -> None:
        ...


class ValidationError(Exception):

    def __init__(self, message: str = ...) -> None:
        ...

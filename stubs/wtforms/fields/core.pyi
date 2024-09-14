"""core.pyi"""
from __future__ import annotations
from typing import Any, Callable


class Field:
    data: Any

    def __init__(self,
                 label: str = ...,
                 validators: list[Callable[[Any, Any], None]] = ...) -> None:
        ...

    def validate(self, form: Any, extra_validators: list[Any] = ...) -> bool:
        ...

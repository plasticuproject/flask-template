"""csrf.pyi"""
from __future__ import annotations
from typing import Any


class CSRFProtect:

    def __init__(self, app: Any = ...) -> None:
        ...

    def init_app(self, app: Any) -> None:
        ...

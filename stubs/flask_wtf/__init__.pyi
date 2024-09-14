"""__init__.pyi"""
from __future__ import annotations
from typing import Any


class Form:

    def validate(self) -> bool:
        ...

    def validate_on_submit(self) -> bool:
        ...


class FlaskForm(Form):
    csrf_token: Any
    meta: Any

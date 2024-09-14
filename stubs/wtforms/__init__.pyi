"""__init__.pyi"""
from __future__ import annotations
from wtforms.fields.core import Field
from typing import Callable, Any


class StringField(Field):

    def __init__(self,
                 label: str = ...,
                 validators: list[Callable[[Any, Any], None]] = ...) -> None:
        ...


class PasswordField(Field):

    def __init__(self,
                 label: str = ...,
                 validators: list[Callable[[Any, Any], None]] = ...) -> None:
        ...


class SubmitField(Field):

    def __init__(self,
                 label: str = ...,
                 validators: list[Callable[[Any, Any], None]] = ...) -> None:
        ...

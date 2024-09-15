"""__init__.pyi"""
from __future__ import annotations
from typing import Any, Callable, TypeVar
from datetime import timedelta

_T = TypeVar("_T")
_T_C = TypeVar("_T_C", bound=Callable[..., Any])


class UserMixin:
    is_authenticated: bool
    is_active: bool
    is_anonymous: bool

    def get_id(self) -> str:
        ...


class LoginManager:

    def __init__(self, app: Any = ...) -> None:
        ...

    def init_app(self, app: Any) -> None:
        ...

    def user_loader(self, callback: Callable[[str],
                                             _T]) -> Callable[[str], _T]:
        ...

    login_view: str | None
    login_message_category: str


login_manager = LoginManager()


def login_user(user: UserMixin,
               remember: bool = False,
               duration: timedelta | None = None,
               force: bool = False,
               fresh: bool = True) -> bool:
    ...


def logout_user() -> bool:
    ...


def login_required(func: _T_C) -> _T_C:
    ...


current_user: Any

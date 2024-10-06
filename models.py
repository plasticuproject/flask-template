"""models.py"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from extensions import db, login_manager

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """
    Load user by ID.

    This function retrieves a user from the database based on their user ID.
    It is used by Flask-Login to load the authenticated user during a request.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        User | None: The user object if found, otherwise `None`.
    """
    return cast(User | None, User.query.get(int(user_id)))


class User(Model, UserMixin):
    """
    User model.

    Represents a user in the system, storing their username, password,
    failed login attempts, and other related information.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's unique username.
        password (str): The user's hashed password.
        failed_attempts (int): The number of failed login attempts.
        lockout_until (datetime | None): The datetime until the user is locked
            out, or `None` if not locked out.
        is_admin (bool): Whether the user has admin privileges.
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150),
                                          nullable=False,
                                          unique=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime)
    failed_attempts: Mapped[int] = mapped_column(default=0)
    lockout_until: Mapped[datetime | None] = mapped_column(DateTime,
                                                           nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __init__(self, username: str, password: str, is_admin: bool = False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.created = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

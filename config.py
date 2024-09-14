"""config.py"""
from __future__ import annotations
from pathlib import Path
from os import environ
from dotenv import load_dotenv

load_dotenv()

APP_PATH = str(Path(__file__).parent.resolve())


def str_to_bool(value: str) -> bool:
    """
    Convert a string to a boolean.

    This function interprets the provided string as a boolean value. It treats
    certain string representations ("true", "1", "t") as `True` and everything
    else as `False`.

    Args:
        value (str): The string to be interpreted as a boolean.

    Returns:
        bool: The boolean representation of the string.
    """
    return value.lower() in ("true", "1", "t")


class Config:
    """
    Configuration settings for the application.

    This class sets various configuration settings based on environment
    variables. In production, certain security-related settings are enabled,
    and the database connection string is sourced from environment variables.

    Attributes:
        DEBUG (bool): Set to `False` in production to disable debug mode.
        SESSION_COOKIE_SECURE (bool): Ensures cookies are only sent over
            HTTPS.
        REMEMBER_COOKIE_SECURE (bool): Ensures "remember me" cookies are
            secure.
        SESSION_COOKIE_HTTPONLY (bool): Prevents JavaScript from accessing
            cookies.
        REMEMBER_COOKIE_HTTPONLY (bool): Makes "remember me" cookies
            HTTP-only.
        SQLALCHEMY_DATABASE_URI (str): The database URI, either from
            environment variables or defaults to a local SQLite database.
        SECRET_KEY (str): Secret key used for session management and
            security.
    """
    if environ["ENVIRONMENT"] == "prod":
        DEBUG = False
        SESSION_COOKIE_SECURE = True
        REMEMBER_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        REMEMBER_COOKIE_HTTPONLY = True
        SQLALCHEMY_DATABASE_URI = environ["SQLALCHEMY_DATABASE_URI"]
    SECRET_KEY = environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{APP_PATH}/site.db"
    str_to_bool(environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False"))

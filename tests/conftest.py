"""conftest.py"""
from __future__ import annotations
from typing import Generator, Callable, Any
import pytest
from flask import Flask
from app import create_app
from models import User
from extensions import db, argon2


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    # Create a test version of the app
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI":
        "sqlite:///:memory:",  # In-memory test database
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for easier testing
    })

    with app.app_context():
        db.create_all()  # Create tables for tests

        # Create a test user
        test_user = User(
            username="testuser",
            password=argon2.generate_password_hash("TestPassword69@!"))
        db.session.add(test_user)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()  # Cleanup tables after tests


@pytest.fixture
def client(app: Flask) -> Any:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> Any:
    return app.test_cli_runner()


@pytest.fixture
def auth(
        client: Any) -> dict[str, Callable[[str, str], Any]
                             | Callable[[], Any]]:

    def login(username: str = "testuser",
              password: str = "TestPassword69@!") -> Any:
        return client.post("/auth/login",
                           data={
                               "username": username,
                               "password": password
                           })

    def logout() -> Any:
        return client.get("/auth/logout")

    return {"login": login, "logout": logout}

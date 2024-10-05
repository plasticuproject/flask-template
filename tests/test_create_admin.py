"""test_create_admin.py"""
from __future__ import annotations
from typing import Generator
import string
from unittest import mock
import pytest
from flask import Flask
from create_admin import (generate_random_password, create_admin_account,
                          run_create_admin)
from models import User


def test_generate_random_password() -> None:
    password = generate_random_password(20)
    assert len(password) == 20
    assert any(char.isdigit() for char in password)
    assert any(char.islower() for char in password)
    assert any(char.isupper() for char in password)
    assert any(char in string.punctuation for char in password)

    # Ensure it doesn't contain problematic characters
    assert '"' not in password
    assert "'" not in password
    assert "\\" not in password

    # Assert that ValueError is raised when length is too short
    with pytest.raises(ValueError, match="Password length must be at least 4"):
        generate_random_password(3)


def test_create_admin_account(app: Flask) -> None:
    with app.app_context():

        # Ensure no admin exists initially
        assert User.query.filter_by(is_admin=True).first() is None

        # Create admin account
        username, password = create_admin_account()

        # Check if admin was created
        admin_user = User.query.filter_by(is_admin=True).first()
        assert admin_user is not None
        assert admin_user.username == username
        assert admin_user.is_admin is True

        # Ensure password was hashed and is different from the plaintext one
        assert username == "admin"
        assert admin_user.password != password

        # Re-run account creation to ensure no second account is created
        username, password = create_admin_account()

        # Check that the function returns None, None since admin already exists
        assert username is None
        assert password is None


@pytest.fixture
def app_with_context(app: Flask) -> Generator[Flask, None, None]:
    """Fixture to create the app context for the test."""
    with app.app_context():
        yield app


def test_run_create_admin_new_account(app_with_context: Flask) -> None:
    # Ensure no admin exists initially
    assert User.query.filter_by(is_admin=True).first() is None

    # Mock the print function to capture the output
    with mock.patch("builtins.print") as mock_print:
        run_create_admin()

        # Check that the admin account was created
        admin_user = User.query.filter_by(is_admin=True).first()
        assert admin_user is not None
        assert admin_user.username == "admin"
        assert admin_user.is_admin is True

        # Check that the correct print statements were called
        mock_print.assert_any_call("----------------------------------------")
        mock_print.assert_any_call("Admin account created!")
        mock_print.assert_any_call("Username: admin")
        # We can't predict the exact password, so we check the structure
        mock_print.assert_any_call(mock.ANY)
        mock_print.assert_any_call(
            "Please change the password after logging in.")
        mock_print.assert_any_call("----------------------------------------")


def test_run_create_admin_existing_account(app_with_context: Flask) -> None:
    # First, create an admin account
    _, _ = create_admin_account()

    # Mock the print function to capture the output
    with mock.patch("builtins.print") as mock_print:
        run_create_admin()

        # Ensure the admin already exists and wasn't recreated
        admin_user = User.query.filter_by(is_admin=True).first()
        assert admin_user is not None
        assert admin_user.username == "admin"
        assert admin_user.is_admin is True

        # Check that the "Admin account already exists." message was printed
        mock_print.assert_any_call("Admin account already exists.")

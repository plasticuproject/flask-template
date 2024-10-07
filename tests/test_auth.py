"""test_auth.py"""
from __future__ import annotations
from typing import Any
from datetime import datetime, timedelta, timezone
from flask import url_for

LOCKOUT_THRESHOLD = 5  # Maximum allowed failed attempts
LOCKOUT_DURATION = timedelta(minutes=15)  # Lockout duration


def test_register(client: Any) -> None:
    # Test GET request to registration page
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Home" in response.data

    # Test successful registration
    response = client.post("/auth/register",
                           data={
                               "username": "newuser",
                               "password": "NewPassword123!",
                               "confirm_password": "NewPassword123!"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Home" in response.data

    # Test registration with existing username
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",  # Same username as before
            "password": "AnotherPassword123!",
            "confirm_password": "AnotherPassword123!"
        },
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Home" in response.data

    # Test registration with mismatched passwords
    response = client.post("/auth/register",
                           data={
                               "username": "anotheruser",
                               "password": "Password123!",
                               "confirm_password": "DifferentPassword!"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be equal to password" in response.data

    # Test registration with invalid username (e.g., too short)
    response = client.post(
        "/auth/register",
        data={
            "username": "ab",  # Assuming minimum length is 3
            "password": "Password123!",
            "confirm_password": "Password123!"
        },
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Home" in response.data


def test_login(client: Any, auth: Any) -> None:
    response = auth["login"]("testuser", "TestPassword69@!")
    assert response.status_code == 302


def test_logout(client: Any, auth: Any) -> None:
    auth["login"]()
    response = auth["logout"]()
    assert response.status_code == 302


def test_login_invalid_username(client: Any, auth: Any) -> None:
    # Test login with a username that doesn"t exist
    response = auth["login"]("nonexistentuser", "SomePassword123!")
    assert response.status_code == 200
    assert b"Home" in response.data


def test_login_invalid_password(client: Any, auth: Any) -> None:
    # Create a user for testing
    auth["register"]("testuser", "CorrectPassword123!")
    # Test login with incorrect password
    response = auth["login"]("testuser", "WrongPassword!")
    assert response.status_code == 200
    assert b"Home" in response.data


def test_account_lockout(client: Any, auth: Any) -> None:
    # Create a user
    auth["register"]("lockoutuser", "SecurePassword123!")
    for _ in range(LOCKOUT_THRESHOLD):
        response = auth["login"]("lockoutuser", "WrongPassword!")

    # Account should now be locked
    response = auth["login"]("lockoutuser", "SecurePassword123!")
    assert b"Home" in response.data


def test_lockout_duration(client: Any, auth: Any, monkeypatch: Any) -> None:
    # Create a user
    auth["register"]("tempuser", "TempPassword123!")
    # Lock the account
    for _ in range(LOCKOUT_THRESHOLD):
        auth["login"]("tempuser", "WrongPassword!")

    # Fast-forward time to after lockout duration
    future_time = datetime.now(
        timezone.utc) + LOCKOUT_DURATION + timedelta(seconds=1)
    monkeypatch.setattr("datetime.datetime",
                        lambda *args, **kwargs: future_time)

    # Try logging in again
    response = auth["login"]("tempuser", "TempPassword123!")
    assert response.status_code == 200


def test_login_next_parameter(client: Any, auth: Any) -> None:
    # Test login with next parameter
    response = client.post("/auth/login?next=/dashboard",
                           data={
                               "username": "testuser",
                               "password": "TestPassword69@!"
                           },
                           follow_redirects=True)
    assert response.request.path == "/dashboard"


def test_login_missing_data(client: Any) -> None:
    response = client.post("/auth/login",
                           data={
                               "username": "",
                               "password": ""
                           },
                           follow_redirects=True)
    assert b"Home" in response.data


def test_register_missing_data(client: Any) -> None:
    response = client.post("/auth/register",
                           data={
                               "username": "",
                               "password": "",
                               "confirm_password": ""
                           },
                           follow_redirects=True)
    assert b"Home" in response.data


def test_login_authenticated_user(client: Any, auth: Any) -> None:
    auth["login"]("testuser", "TestPassword69@!")
    response = client.get("/auth/login", follow_redirects=True)
    assert response.request.path == url_for("main.home")
    assert b"Home" in response.data


def test_register_authenticated_user(client: Any, auth: Any) -> None:
    auth["login"]("testuser", "TestPassword69@!")
    response = client.get("/auth/register", follow_redirects=True)
    assert response.request.path == url_for("main.home")
    assert b"Home" in response.data

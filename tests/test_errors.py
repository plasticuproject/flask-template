"""test_errors.py"""
from __future__ import annotations
from typing import Any
import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "url, expected_status_code",
    [
        ("/non-existent-url", 404),  # For testing 404 error
    ])
def test_404_error(client: FlaskClient[Any], url: str,
                   expected_status_code: int) -> None:
    """
    Test the 404 error handler by requesting a non-existent URL.

    Args:
        client (FlaskClient): The test client.
        url (str): The URL to test.
        expected_status_code (int): The expected status code for the response.
    """
    response = client.get(url)
    assert response.status_code == expected_status_code
    assert b"Page Not Found" in response.data


def test_500_error(client: FlaskClient[Any], app: Flask) -> None:
    """
    Test the 500 error handler by triggering an internal server error.

    Args:
        client (FlaskClient): The test client.
        app (Flask): The Flask application instance.
    """
    # Simulate an internal server error.
    @app.route("/trigger-500")
    def trigger_500() -> str:
        raise Exception("This is a test exception")

    # Help mypy understand the correct type for the view function
    app.add_url_rule("/trigger-500", view_func=trigger_500)

    # Ensure that Flask handles the exception and triggers the error handler.
    app.config["TESTING"] = False
    app.config[
        "PROPAGATE_EXCEPTIONS"] = False  # Ensure Flask catches the exception

    # Now trigger the error and check the response
    response = client.get("/trigger-500")
    assert response.status_code == 500
    assert b"ERROR" in response.data

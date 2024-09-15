"""test_main.py"""
from __future__ import annotations
from typing import Any


def test_home(client: Any) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_dashboard_redirect(client: Any, auth: Any) -> None:
    response = client.get("/dashboard")
    assert response.status_code == 302


def test_dashboard(client: Any, auth: Any) -> None:
    auth["login"]()
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    _ = auth["logout"]()

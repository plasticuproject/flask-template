"""test_auth.py"""
from __future__ import annotations
from typing import Any


def test_login(client: Any, auth: Any) -> None:
    response = auth["login"]("testuser", "TestPassword69@!")
    assert response.status_code == 302


def test_logout(client: Any, auth: Any) -> None:
    auth["login"]()
    response = auth["logout"]()
    assert response.status_code == 302

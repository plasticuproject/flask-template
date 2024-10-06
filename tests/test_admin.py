"""test_admin.py"""
from __future__ import annotations
from typing import Any
from datetime import datetime, timedelta, timezone
from extensions import db, argon2
from create_admin import generate_random_password
from models import User


def generate_accounts() -> tuple[str, str]:
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        existing_admin.is_admin = 0
    admin_username = "testadmin"
    admin_password = generate_random_password()
    hashed_admin_password = argon2.generate_password_hash(admin_password)
    now = datetime.now(timezone.utc)

    # Create new admin user
    new_admin = User(username=admin_username,
                     password=hashed_admin_password,
                     is_admin=True)
    db.session.add(new_admin)

    test_user = User.query.filter_by(username="testuser").first()
    if test_user:
        test_user.failed_attempts = 5
        test_user.lockout_until = now + timedelta(minutes=15)

    db.session.commit()

    return admin_password, test_user.id


def test_reset_lockout(client: Any, auth: Any) -> None:
    admin_password, test_user_id = generate_accounts()
    _ = auth["login"]("testadmin", admin_password)
    client.post(f"/admin/reset_lockout/{test_user_id}")
    test_user = User.query.filter_by(username="testuser").first()
    if test_user:
        assert test_user.lockout_until is None
    _ = auth["logout"]()


def test_rest_lockout_redirect(client: Any, auth: Any) -> None:
    _ = auth["login"]()
    response = client.post("/admin/reset_lockout/2")
    assert response.status_code == 302

"""create_admin.py"""
from __future__ import annotations
import string
import random
from app import create_app
from extensions import db, argon2
from models import User


def generate_random_password(length: int = 20) -> str:
    """
    Generate a random password containing letters, digits, and punctuation.

    The function creates a password of the specified length using a combination
    of uppercase and lowercase letters, digits, and punctuation. Some
    problematic characters like double quotes, single quotes, and backslashes
    are excluded from the set of characters used.

    Args:
        length (int, optional): The length of the password. Defaults to 20.

    Returns:
        str: The generated random password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation

    # Exclude problematic characters
    characters = characters.replace('"', "").replace("'", "").replace("\\", "")
    password = "".join(random.choice(characters) for _ in range(length))
    return password


app = create_app()

with app.app_context():

    # Check for existing admin account
    admin_user = User.query.filter_by(is_admin=True).first()
    if not admin_user:
        # Create default admin credentials
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = generate_random_password()
        hashed_password = argon2.generate_password_hash(ADMIN_PASSWORD)

        # Create new admin user
        new_admin = User(username=ADMIN_USERNAME,
                         password=hashed_password,
                         is_admin=True)
        db.session.add(new_admin)
        db.session.commit()

        # Print admin credentials to the terminal
        print("----------------------------------------")
        print("Admin account created!")
        print(f"Username: {ADMIN_USERNAME}")
        print(f"Password: {ADMIN_PASSWORD}")
        print("Please change the password after logging in.")
        print("----------------------------------------")

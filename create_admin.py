"""create_admin.py"""
from __future__ import annotations
import string
import random
from app import create_app
from extensions import db, argon2
from models import User


def generate_random_password(length: int = 20) -> str:
    """
    Generate a random password containing at least one lowercase letter,
    one uppercase letter, one digit, and one punctuation character.

    Args:
        length (int): Length of the password. Default is 20.

    Returns:
        str: The generated random password.
    """
    if length < 4:
        raise ValueError(
            "Password length must be at least 4 to include all character types"
        )

    # Separate character pools
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation.replace('"',
                                             "").replace("'",
                                                         "").replace("\\", "")

    # Ensure password contains at least one of each required character type
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(punctuation)
    ]

    # Fill the rest of the password length with random characters from all pools
    all_characters = lower + upper + digits + punctuation
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the password list to avoid predictable placement of characters
    random.shuffle(password)

    return ''.join(password)


def create_admin_account() -> tuple[str | None, str | None]:
    """
    Create an admin account with a random password, if one doesn't exist.

    Returns:
        tuple (str | None, str | None): A tuple containing the admin
            username and password.
    """
    # Check for existing admin account
    admin_user = User.query.filter_by(is_admin=True).first()
    if admin_user:
        print(f"Admin already exists: {admin_user.username}")  # Debugging line
        return None, None
    admin_username = "admin"
    admin_password = generate_random_password()
    hashed_password = argon2.generate_password_hash(admin_password)

    # Create new admin user
    new_admin = User(username=admin_username,
                     password=hashed_password,
                     is_admin=True)
    db.session.add(new_admin)
    db.session.commit()

    return admin_username, admin_password


def run_create_admin() -> None:
    app = create_app()
    with app.app_context():
        username, password = create_admin_account()
        if username and password:
            print("----------------------------------------")
            print("Admin account created!")
            print(f"Username: {username}")
            print(f"Password: {password}")
            print("Please change the password after logging in.")
            print("----------------------------------------")
        else:
            print("Admin account already exists.")


if __name__ == "__main__":
    run_create_admin()

"""forms.py"""
from __future__ import annotations
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Length, EqualTo, Regexp,
                                ValidationError)
from wtforms.fields.core import Field
from models import User


class RegistrationForm(FlaskForm):
    """
    Registration form for new users.

    This form collects the necessary information for a new user to register,
    including a username, password, and password confirmation. Passwords are
    validated to ensure they meet security requirements, and the username is
    checked to ensure it is unique.

    Attributes:
        username (StringField): The username field, requiring a unique username
            with a length between 8 and 150 characters.
        password (PasswordField): The password field, requiring a password with
            at least one uppercase letter, one lowercase letter, one number,
            and one special character, with a minimum length of 8 characters.
        confirm_password (PasswordField): A confirmation password field,
            requiring the same value as the password field.
        submit (SubmitField): The submit button for the form.

    Methods:
        validate_username: Validates whether the username is already in use by
            checking the database. Raises a `ValidationError` if the username
            is taken.
    """
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=8, max=150)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(
                '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*()_+\\-=\\[\\]{};\'":\\\\|,.<>\\/?]).+$',
                message=(
                    "Password must contain at least one uppercase letter, one "
                    "lowercase letter, one number, and one special character."
                ))
        ])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(),
                                        EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username: Field) -> None:
        """
        Ensure the username is not already taken.

        This method checks the database to see if the username provided in the
        form already exists. If it does, a `ValidationError` is raised.

        Args:
            username (Field): The form field for the username to validate.

        Raises:
            ValidationError: If the username already exists in the database.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken.")


class LoginForm(FlaskForm):
    """
    Login form for existing users.

    This form collects the necessary information for a user to log in,
    including a username and password.

    Attributes:
        username (StringField): The username field, requiring a username with
            a length between 4 and 150 characters.
        password (PasswordField): The password field, requiring a valid
            password.
        submit (SubmitField): The submit button for the form.
    """
    username: StringField = StringField(
        "Username", validators=[DataRequired(),
                                Length(min=4, max=150)])
    password: PasswordField = PasswordField("Password",
                                            validators=[DataRequired()])
    submit: SubmitField = SubmitField("Login")

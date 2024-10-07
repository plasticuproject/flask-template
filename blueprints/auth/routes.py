"""routes.py"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urljoin
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.wrappers import Response
from extensions import db, argon2
from models import User
from . import auth_bp
from .forms import RegistrationForm, LoginForm

LOCKOUT_THRESHOLD = 5  # Maximum allowed failed attempts
LOCKOUT_DURATION = timedelta(minutes=15)  # Lockout duration
MAIN_HOME = "main.home"
allowed_next_page = ["/dashboard"]


def is_safe_url(target: str) -> bool:
    """
    Check if a URL is safe for redirection.

    Args:
        target (str): The target URL to validate.

    Returns:
        bool: True if the URL is safe, False otherwise.
    """
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and \
        host_url.netloc == redirect_url.netloc and \
        target in allowed_next_page


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """
    Handle user registration.

    This route allows users to register for an account. If the user is already
    authenticated, they are redirected to the home page. On successful
    registration, the user's account is created and stored in the database,
    and they are redirected to the login page.

    Returns:
        str | Response: Redirects to the home page if the user is already
        authenticated or redirects to the login page after successful
        registration. If the registration form is invalid, renders the
        registration page.
    """
    if request.method == "GET" and current_user.is_authenticated:
        return redirect(url_for(MAIN_HOME))

    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = argon2.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """
    Handle user login.

    This route allows users to log in to their account. If the user is already
    authenticated, they are redirected to the home page. The route checks the
    provided username and password, manages failed login attempts, and
    enforces account lockout after a set threshold. On successful login, the
    user is redirected to the home page or to a next page if provided.

    Returns:
        str | Response: Redirects to the home page if the user is already
        authenticated or logged in successfully. If the login fails, renders
        the login page with appropriate error messages.
    """

    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for(MAIN_HOME))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            now = datetime.now(timezone.utc)

            # Check if user exists
            if user:
                # Check if account is locked
                if user.lockout_until:
                    if user.lockout_until.tzinfo is None:
                        # Assume the naive datetime is in UTC
                        user.lockout_until = user.lockout_until.replace(
                            tzinfo=timezone.utc)
                    if user.lockout_until > now:
                        remaining = user.lockout_until - now
                        flash(
                            "Account is locked. Try again in "
                            f"{remaining.seconds // 60} minutes.", "danger")
                        return render_template("login.html", form=form)

                # Verify password
                if argon2.check_password_hash(user.password,
                                              form.password.data):
                    # Reset failed attempts
                    user.failed_attempts = 0
                    user.lockout_until = None
                    db.session.commit()

                    login_user(user)
                    flash("Logged in successfully.", "success")
                    next_page = request.args.get("next")
                    if next_page and is_safe_url(next_page):
                        return redirect(next_page)
                    return redirect(url_for(MAIN_HOME))

                # Increment failed attempts
                user.failed_attempts += 1

                if user.failed_attempts >= LOCKOUT_THRESHOLD:
                    user.lockout_until = now + LOCKOUT_DURATION
                    flash(
                        "Account locked due to too many failed login "
                        "attempts. Please try again later.", "danger")
                else:
                    attempts_left = LOCKOUT_THRESHOLD - user.failed_attempts
                    flash(
                        f"Login unsuccessful. You have {attempts_left} "
                        "more attempt(s) before account lockout.", "danger")

                db.session.commit()
            else:
                flash(
                    "Login unsuccessful. Please check username and password.",
                    "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> str | Response:
    """
    Handle user logout.

    This route logs out the currently authenticated user. After logging out,
    the user is redirected to the home page with a notification.

    Returns:
        str | Response: Redirects to the home page after logout.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for(MAIN_HOME))

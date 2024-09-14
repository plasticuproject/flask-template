"""routes.py"""
from __future__ import annotations
from flask import render_template
from werkzeug.wrappers import Response
from flask_login import login_required
from . import main_bp


@main_bp.route("/")
def home() -> str | Response:
    """
    Render the home page.

    This route renders the main home page of the application.

    Returns:
        str | Response: The rendered home page template.
    """
    return render_template("home.html")


@main_bp.route("/dashboard")
@login_required
def dashboard() -> str | Response:
    """
    Render the dashboard page.

    This route renders the dashboard page, but only for authenticated users.
    Users must be logged in to access this route.

    Returns:
        str | Response: The rendered dashboard page template.
    """
    return render_template("dashboard.html")

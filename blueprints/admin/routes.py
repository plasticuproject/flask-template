"""routes.py"""
from __future__ import annotations
from flask import redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from werkzeug.wrappers import Response
from extensions import db
from models import User
from . import admin_bp


@admin_bp.route("/reset_lockout/<int:user_id>", methods=["POST"])
@login_required
def reset_lockout(user_id: str) -> str | Response:
    """
    Reset the lockout status of a user.

    This route allows an admin to reset the failed login attempts and lockout
    time of a user. The function checks if the current user is an admin before
    proceeding. If the current user is not an admin, they are redirected to
    the home page with an "Access denied" message.

    Args:
        user_id (str): The ID of the user whose lockout is being reset.

    Returns:
        str | Response: Redirects to the home page if access is denied or to
        the user management page after a successful reset.
    """
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("main.home"))

    user = User.query.get_or_404(user_id)
    user.failed_attempts = 0
    user.lockout_until = None
    db.session.commit()
    flash(f"Lockout reset for user {user.username}.", "success")
    # return redirect(url_for("admin.user_management"))
    return redirect(url_for("main.home"))

"""handlers.py"""
from __future__ import annotations
from flask import render_template
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound, InternalServerError
from . import errors_bp


@errors_bp.app_errorhandler(404)  # type: ignore
def page_not_found(e: NotFound) -> tuple[str, int] | Response:
    """
    Handle 404 errors by rendering the 'page not found' template.

    This route is triggered when a 404 (Not Found) error occurs. It renders
    a custom '404.html' template.

    Args:
        e (NotFound): The 404 error that triggered this handler.

    Returns:
        tuple[str, int] | Response: The rendered '404.html' template and the
        404 status code.
    """
    return render_template('404.html'), 404


@errors_bp.app_errorhandler(500)  # type: ignore
def internal_server_error(
        e: InternalServerError) -> tuple[str, int] | Response:
    """
    Handle 500 errors by rendering the 'internal server error' template.

    This route is triggered when a 500 (Internal Server Error) occurs. It
    renders a custom '500.html' template.

    Args:
        e (InternalServerError): The 500 error that triggered this handler.

    Returns:
        tuple[str, int] | Response: The rendered '500.html' template and the
        500 status code.
    """
    return render_template('500.html'), 500

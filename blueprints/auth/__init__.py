"""__init__.py"""
from __future__ import annotations
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


from . import routes

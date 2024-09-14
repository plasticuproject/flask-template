"""__init__>py"""
from __future__ import annotations
from flask import Blueprint

errors_bp = Blueprint("errors", __name__, template_folder="templates")

from . import handlers

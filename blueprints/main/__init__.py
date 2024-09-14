"""__init__.py"""
from __future__ import annotations
from flask import Blueprint

main_bp = Blueprint("main",
                    __name__,
                    template_folder="templates",
                    static_folder="static")

from . import routes

"""extensions.py"""
from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_argon2 import Argon2
from flask_migrate import Migrate

db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager()
csrf: CSRFProtect = CSRFProtect()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
argon2: Argon2 = Argon2()
migrate: Migrate = Migrate()

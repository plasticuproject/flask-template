"""app.py"""
from __future__ import annotations
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from extensions import db, login_manager, csrf, migrate, argon2
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.errors import errors_bp


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function sets up the Flask application, initializes various
    extensions (database, login manager, CSRF protection, password hashing,
    and migrations), and registers blueprints for different parts of the
    application.

    The app is configured from the `Config` object, and certain middleware,
    such as `ProxyFix`, is applied.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    argon2.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(errors_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

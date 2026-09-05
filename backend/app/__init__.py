from flask import Flask
from flask_cors import CORS

from app.utils.exceptions import register_error_handlers


def create_app():
    app = Flask(__name__)

    CORS(app)
    register_error_handlers(app)

    from app.routes.health_route import health_bp
    from app.routes.users_route import users_bp

    app.register_blueprint(
        health_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        users_bp,
        url_prefix="/api/users"
    )

    return app

from flask import Flask
from flask_cors import CORS

from app.utils.exceptions import register_error_handlers


def create_app():
    app = Flask(__name__)

    CORS(app)
    register_error_handlers(app)

    from app.routes.health_route import health_bp
    from app.routes.image_route import image_bp
    from app.routes.users_route import users_bp
    from app.routes.album_routes import album_bp
    from app.routes.tag_routes import tag_bp
    from app.routes.favorite_routes import favorite_bp
    from app.routes.people_routes import people_bp
    from app.routes.search_routes import search_bp
    from app.routes.auth_route import auth_bp
    from app.routes.telegram_route import telegram_bp

    app.register_blueprint(
        health_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        users_bp,
        url_prefix="/api/users"
    )

    app.register_blueprint(
        image_bp,
        url_prefix="/api/images"
    )

    app.register_blueprint(
        album_bp,
        url_prefix="/api/albums"
    )

    app.register_blueprint(
        tag_bp,
        url_prefix="/api/tags"
    )

    app.register_blueprint(
        favorite_bp,
        url_prefix="/api/favorites"
    )

    app.register_blueprint(
        people_bp,
        url_prefix="/api/people"
    )

    app.register_blueprint(
        search_bp,
        url_prefix="/api/search"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        telegram_bp,
        url_prefix="/api/telegram"
    )

    return app

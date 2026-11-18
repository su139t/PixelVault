from flask import Blueprint

from app.controllers.auth_controller import (
    telegram_login_controller,
    get_me_controller,
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/telegram")
def telegram_login():
    return telegram_login_controller()


@auth_bp.get("/me")
def get_me():
    return get_me_controller()

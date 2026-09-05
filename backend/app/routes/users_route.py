from flask import Blueprint

from app.controllers.users_controller import (
    create_user_controller,
    get_users_controller
)


users_bp = Blueprint(
    "users",
    __name__
)


@users_bp.get("")
def get_users():
    return get_users_controller()


@users_bp.post("")
def create_user():
    return create_user_controller()

from flask import Blueprint

from app.controllers.users_controller import (
    create_user_controller,
    get_users_controller,
    get_user_by_id_controller,
    update_user_controller,
    delete_user_controller
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


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    return get_user_by_id_controller(user_id)


@users_bp.put("/<int:user_id>")
def update_user(user_id):
    return update_user_controller(user_id)


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    return delete_user_controller(user_id)


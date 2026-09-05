from flask import jsonify, request

from app.services.users_service import (
    create_new_user,
    get_users
)
from app.utils.responses import success_response


def create_user_controller():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    user = create_new_user(
        telegram_user_id=data.get("telegram_user_id"),
        name=data.get("name"),
        username=data.get("username"),
        email=data.get("email")
    )

    return success_response(
        data={"user": serialize_user(user)},
        message="User created successfully",
        status_code=201
    )


def get_users_controller():
    users = get_users()

    return success_response(
        data={"users": [serialize_user(user) for user in users]}
    )


def serialize_user(user):
    return {
        "user_id": user[0],
        "telegram_user_id": user[1],
        "name": user[2],
        "username": user[3],
        "email": user[4],
        "created_at": user[5].isoformat() if user[5] else None
    }

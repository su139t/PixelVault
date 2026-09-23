from flask import jsonify, request

from app.services.auth_service import (
    validate_telegram_login,
    find_or_create_user,
    generate_token,
    verify_token,
)
from app.services.users_service import get_user_by_id
from app.utils.responses import success_response, error_response


def telegram_login_controller():
    """Handle Telegram Login Widget callback."""
    data = request.get_json()

    if not data:
        return error_response("Request body is required", 400)

    try:
        # Validate the Telegram hash
        validate_telegram_login(data)

        # Find or create user
        user = find_or_create_user(data)

        # Generate auth token
        token = generate_token(user)

        return success_response(
            data={
                "user": serialize_auth_user(user, data),
                "token": token,
            },
            message="Login successful",
        )
    except ValueError as e:
        return error_response(str(e), 401)


def get_me_controller():
    """Return current authenticated user from token."""
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return error_response("Missing or invalid Authorization header", 401)

    token = auth_header.split(" ", 1)[1]

    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        user = get_user_by_id(user_id)

        return success_response(
            data={"user": serialize_auth_user(user)}
        )
    except ValueError as e:
        return error_response(str(e), 401)


def serialize_auth_user(user, telegram_data=None):
    """Serialize user tuple for auth responses."""
    result = {
        "user_id": user[0],
        "telegram_user_id": user[1],
        "name": user[2],
        "username": user[3],
        "email": user[4],
        "created_at": user[5].isoformat() if user[5] else None,
    }

    # Include photo_url from Telegram data if available
    if telegram_data and telegram_data.get("photo_url"):
        result["photo_url"] = telegram_data["photo_url"]

    return result

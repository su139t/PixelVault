from app.repositories.users_repository import (
    create_user,
    get_all_users
)


def create_new_user(
    telegram_user_id,
    name,
    username=None,
    email=None
):
    if not telegram_user_id:
        raise ValueError(
            "telegram_user_id is required"
        )

    if not name:
        raise ValueError(
            "name is required"
        )

    return create_user(
        telegram_user_id,
        name,
        username,
        email
    )


def get_users():
    return get_all_users()

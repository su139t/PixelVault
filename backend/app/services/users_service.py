from app.repositories.users_repository import (
    create_user,
    get_all_users,
    get_user_by_id as repo_get_user_by_id,
    update_user as repo_update_user,
    delete_user as repo_delete_user
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


def get_user_by_id(user_id):
    """Get a single user. Raises ValueError if not found."""
    user = repo_get_user_by_id(user_id)

    if not user:
        raise ValueError(f"User with id {user_id} not found")

    return user


def update_user(user_id, name=None, username=None, email=None):
    """Update user fields. Raises ValueError if user not found."""
    # First check user exists
    existing = repo_get_user_by_id(user_id)
    if not existing:
        raise ValueError(f"User with id {user_id} not found")

    updated = repo_update_user(
        user_id,
        name=name,
        username=username,
        email=email
    )

    return updated


def delete_user(user_id):
    """Delete a user. Raises ValueError if not found."""
    deleted = repo_delete_user(user_id)

    if not deleted:
        raise ValueError(f"User with id {user_id} not found")

    return deleted


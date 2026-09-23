from app.db import get_db_connection


USER_COLUMNS = """
    user_id,
    telegram_user_id,
    name,
    username,
    email,
    created_at
"""


def create_user(
    telegram_user_id,
    name,
    username,
    email
):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (
                    telegram_user_id,
                    name,
                    username,
                    email
                )
                VALUES (%s, %s, %s, %s)
                RETURNING
                    {columns};
            """.format(columns=USER_COLUMNS), (
                telegram_user_id,
                name,
                username,
                email
            ))

            user = cursor.fetchone()

        conn.commit()

        return user

    finally:
        conn.close()


def get_all_users():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    {columns}
                FROM users
                ORDER BY user_id;
            """.format(columns=USER_COLUMNS))

            return cursor.fetchall()
    finally:
        conn.close()


def get_user_by_id(user_id):
    """Fetch a single user by their user_id."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    {columns}
                FROM users
                WHERE user_id = %s;
            """.format(columns=USER_COLUMNS), (user_id,))

            return cursor.fetchone()
    finally:
        conn.close()


def update_user(user_id, name=None, username=None, email=None):
    """Update user fields. Only provided (non-None) fields are updated."""
    # Build SET clause dynamically — only update fields that were passed
    fields = []
    values = []

    if name is not None:
        fields.append("name = %s")
        values.append(name)

    if username is not None:
        fields.append("username = %s")
        values.append(username)

    if email is not None:
        fields.append("email = %s")
        values.append(email)

    if not fields:
        raise ValueError("At least one field must be provided for update")

    # Always update updated_at timestamp
    fields.append("updated_at = CURRENT_TIMESTAMP")

    # Add user_id as the last parameter for WHERE clause
    values.append(user_id)

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET {set_clause}
                WHERE user_id = %s
                RETURNING
                    {columns};
            """.format(
                set_clause=", ".join(fields),
                columns=USER_COLUMNS
            ), tuple(values))

            user = cursor.fetchone()

        conn.commit()

        return user

    finally:
        conn.close()


def delete_user(user_id):
    """Delete a user by user_id. Returns the deleted user row."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM users
                WHERE user_id = %s
                RETURNING
                    {columns};
            """.format(columns=USER_COLUMNS), (user_id,))

            user = cursor.fetchone()

        conn.commit()

        return user

    finally:
        conn.close()


def get_user_by_telegram_id(telegram_user_id):
    """Fetch a single user by their telegram_user_id."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    {columns}
                FROM users
                WHERE telegram_user_id = %s;
            """.format(columns=USER_COLUMNS), (telegram_user_id,))

            return cursor.fetchone()
    finally:
        conn.close()


def upsert_user(telegram_user_id, name, username=None):
    """Insert a new user or update existing by telegram_user_id."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (
                    telegram_user_id,
                    name,
                    username
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (telegram_user_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    username = COALESCE(EXCLUDED.username, users.username),
                    updated_at = CURRENT_TIMESTAMP
                RETURNING
                    {columns};
            """.format(columns=USER_COLUMNS), (
                telegram_user_id,
                name,
                username,
            ))

            user = cursor.fetchone()

        conn.commit()

        return user

    finally:
        conn.close()


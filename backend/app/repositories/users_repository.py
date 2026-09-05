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

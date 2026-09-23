from app.db import get_db_connection


FAVORITE_COLUMNS = """
    favorite_id,
    user_id,
    image_id,
    created_at
"""


def add_favorite(user_id, image_id):
    """Add an image to user's favorites."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO favorites (user_id, image_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, image_id) DO NOTHING
                RETURNING {columns};
            """.format(columns=FAVORITE_COLUMNS), (user_id, image_id))

            favorite = cursor.fetchone()

        conn.commit()
        return favorite

    finally:
        conn.close()


def remove_favorite(user_id, image_id):
    """Remove an image from user's favorites."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM favorites
                WHERE user_id = %s AND image_id = %s
                RETURNING {columns};
            """.format(columns=FAVORITE_COLUMNS), (user_id, image_id))

            favorite = cursor.fetchone()

        conn.commit()
        return favorite

    finally:
        conn.close()


def get_user_favorites(user_id):
    """Get all favorite images for a user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    i.image_id,
                    i.user_id,
                    i.title,
                    i.file_name,
                    i.mime_type,
                    i.width,
                    i.height,
                    i.file_size,
                    i.telegram_chat_id,
                    i.telegram_message_id,
                    i.ai_description,
                    i.detected_text,
                    i.visibility,
                    i.upload_date
                FROM images i
                JOIN favorites f ON i.image_id = f.image_id
                WHERE f.user_id = %s
                ORDER BY f.created_at DESC;
            """, (user_id,))

            return cursor.fetchall()
    finally:
        conn.close()

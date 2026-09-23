from app.db import get_db_connection


ALBUM_COLUMNS = """
    album_id,
    user_id,
    album_name,
    created_at
"""


def create_album(user_id, album_name):
    """Insert a new album for the given user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO albums (user_id, album_name)
                VALUES (%s, %s)
                RETURNING {columns};
            """.format(columns=ALBUM_COLUMNS), (user_id, album_name))

            album = cursor.fetchone()

        conn.commit()
        return album

    finally:
        conn.close()


def get_all_albums(user_id):
    """Get all albums for a user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM albums
                WHERE user_id = %s
                ORDER BY created_at DESC;
            """.format(columns=ALBUM_COLUMNS), (user_id,))

            return cursor.fetchall()
    finally:
        conn.close()


def get_album_by_id(album_id):
    """Get a single album by ID."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM albums
                WHERE album_id = %s;
            """.format(columns=ALBUM_COLUMNS), (album_id,))

            return cursor.fetchone()
    finally:
        conn.close()


def update_album(album_id, album_name):
    """Rename an album."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE albums
                SET album_name = %s
                WHERE album_id = %s
                RETURNING {columns};
            """.format(columns=ALBUM_COLUMNS), (album_name, album_id))

            album = cursor.fetchone()

        conn.commit()
        return album

    finally:
        conn.close()


def delete_album(album_id):
    """Delete an album. Images in the album will have album_id set to NULL (ON DELETE SET NULL)."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM albums
                WHERE album_id = %s
                RETURNING {columns};
            """.format(columns=ALBUM_COLUMNS), (album_id,))

            album = cursor.fetchone()

        conn.commit()
        return album

    finally:
        conn.close()


def add_image_to_album(album_id, image_id):
    """Assign an image to an album by updating image's album_id."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE images
                SET album_id = %s, updated_at = CURRENT_TIMESTAMP
                WHERE image_id = %s
                RETURNING image_id;
            """, (album_id, image_id))

            result = cursor.fetchone()

        conn.commit()
        return result

    finally:
        conn.close()


def remove_image_from_album(album_id, image_id):
    """Remove an image from an album (set album_id to NULL)."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE images
                SET album_id = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE image_id = %s AND album_id = %s
                RETURNING image_id;
            """, (image_id, album_id))

            result = cursor.fetchone()

        conn.commit()
        return result

    finally:
        conn.close()


def get_album_images(album_id):
    """Get all images in an album."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    image_id,
                    user_id,
                    title,
                    description,
                    file_name,
                    mime_type,
                    width,
                    height,
                    file_size,
                    telegram_chat_id,
                    telegram_message_id,
                    ai_description,
                    detected_text,
                    album_id,
                    visibility,
                    upload_date,
                    updated_at
                FROM images
                WHERE album_id = %s
                ORDER BY upload_date DESC;
            """, (album_id,))

            return cursor.fetchall()
    finally:
        conn.close()

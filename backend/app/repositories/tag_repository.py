from app.db import get_db_connection


TAG_COLUMNS = """
    tag_id,
    user_id,
    tag_name,
    created_at
"""


def create_tag(user_id, tag_name):
    """Insert a new tag for the given user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tags (user_id, tag_name)
                VALUES (%s, %s)
                RETURNING {columns};
            """.format(columns=TAG_COLUMNS), (user_id, tag_name))

            tag = cursor.fetchone()

        conn.commit()
        return tag

    finally:
        conn.close()


def get_all_tags(user_id):
    """Get all tags for a user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM tags
                WHERE user_id = %s
                ORDER BY tag_name;
            """.format(columns=TAG_COLUMNS), (user_id,))

            return cursor.fetchall()
    finally:
        conn.close()


def get_tag_by_id(tag_id):
    """Get a single tag by ID."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM tags
                WHERE tag_id = %s;
            """.format(columns=TAG_COLUMNS), (tag_id,))

            return cursor.fetchone()
    finally:
        conn.close()


def delete_tag(tag_id):
    """Delete a tag. Cascade removes image_tags entries too."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM tags
                WHERE tag_id = %s
                RETURNING {columns};
            """.format(columns=TAG_COLUMNS), (tag_id,))

            tag = cursor.fetchone()

        conn.commit()
        return tag

    finally:
        conn.close()


def add_tag_to_image(image_id, tag_id):
    """Associate a tag with an image in image_tags junction table."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO image_tags (image_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT (image_id, tag_id) DO NOTHING
                RETURNING image_id, tag_id;
            """, (image_id, tag_id))

            result = cursor.fetchone()

        conn.commit()
        return result

    finally:
        conn.close()


def remove_tag_from_image(image_id, tag_id):
    """Remove a tag-image association."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM image_tags
                WHERE image_id = %s AND tag_id = %s
                RETURNING image_id, tag_id;
            """, (image_id, tag_id))

            result = cursor.fetchone()

        conn.commit()
        return result

    finally:
        conn.close()


def get_tags_for_image(image_id):
    """Get all tags for a specific image."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    t.tag_id,
                    t.user_id,
                    t.tag_name,
                    t.created_at
                FROM tags t
                JOIN image_tags it ON t.tag_id = it.tag_id
                WHERE it.image_id = %s
                ORDER BY t.tag_name;
            """, (image_id,))

            return cursor.fetchall()
    finally:
        conn.close()

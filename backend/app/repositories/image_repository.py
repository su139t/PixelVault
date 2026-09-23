from app.db import get_db_connection


IMAGE_COLUMNS = """
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
"""


def create_image_record(
    user_id,
    title,
    telegram_chat_id,
    telegram_message_id,
    file_name,
    mime_type,
    width,
    height,
    file_size,
    unique_id, # Keeping this parameter for backward compatibility if needed by service, but not inserting it as it's not in schema
):
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO images (
                    user_id,
                    title,
                    telegram_chat_id,
                    telegram_message_id,
                    file_name,
                    mime_type,
                    width,
                    height,
                    file_size
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    user_id,
                    title,
                    telegram_chat_id,
                    telegram_message_id,
                    file_name,
                    mime_type,
                    width,
                    height,
                    file_size,
                ),
            )
            image = cursor.fetchone()
        conn.commit()
        return image
    finally:
        conn.close()


def get_all_images(user_id):
    """Get all images for a user, ordered by upload date descending."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM images
                WHERE user_id = %s
                ORDER BY upload_date DESC;
            """.format(columns=IMAGE_COLUMNS), (user_id,))
            return cursor.fetchall()
    finally:
        conn.close()


def get_image_by_id(image_id):
    """Get a single image by ID."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM images
                WHERE image_id = %s;
            """.format(columns=IMAGE_COLUMNS), (image_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def update_image(image_id, title=None, description=None, visibility=None, album_id=None):
    """Update editable image fields."""
    fields = []
    values = []

    if title is not None:
        fields.append("title = %s")
        values.append(title)
        
    if description is not None:
        fields.append("description = %s")
        values.append(description)

    if visibility is not None:
        fields.append("visibility = %s")
        values.append(visibility)
        
    # allow updating album_id (can be None/null)
    # Using a sentinel value would be better, but for simplicity we assume 
    # if album_id is explicitly passed, we update it. But python kwargs default to None.
    # To properly handle setting album_id to NULL, the service needs to pass a special value or 
    # we just provide a separate remove_from_album function (which we did in album_repo).
    # We will skip album_id here and let album routes handle it.

    if not fields:
        return get_image_by_id(image_id)

    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(image_id)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE images
                SET {set_clause}
                WHERE image_id = %s
                RETURNING {columns};
            """.format(
                set_clause=", ".join(fields),
                columns=IMAGE_COLUMNS
            ), tuple(values))
            
            image = cursor.fetchone()
        conn.commit()
        return image
    finally:
        conn.close()


def delete_image(image_id):
    """Delete an image record."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM images
                WHERE image_id = %s
                RETURNING telegram_chat_id, telegram_message_id;
            """, (image_id,))
            deleted = cursor.fetchone()
        conn.commit()
        return deleted
    finally:
        conn.close()


def add_face_to_image(image_id, person_id, bounding_box=None, confidence=None):
    """Link a recognized face/person to an image."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO image_faces (image_id, person_id, bounding_box, confidence)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (image_id, person_id) 
                DO UPDATE SET 
                    bounding_box = EXCLUDED.bounding_box,
                    confidence = EXCLUDED.confidence
                RETURNING image_id, person_id;
            """, (image_id, person_id, bounding_box, confidence))
            
            result = cursor.fetchone()
        conn.commit()
        return result
    finally:
        conn.close()
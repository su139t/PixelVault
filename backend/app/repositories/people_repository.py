from app.db import get_db_connection


PEOPLE_COLUMNS = """
    person_id,
    user_id,
    person_name,
    compreface_subject_id,
    created_at
"""


def create_person(user_id, person_name, compreface_subject_id=None):
    """Insert a new person."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO people (user_id, person_name, compreface_subject_id)
                VALUES (%s, %s, %s)
                RETURNING {columns};
            """.format(columns=PEOPLE_COLUMNS), (user_id, person_name, compreface_subject_id))

            person = cursor.fetchone()

        conn.commit()
        return person

    finally:
        conn.close()


def get_all_people(user_id):
    """Get all recognized people for a user."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM people
                WHERE user_id = %s
                ORDER BY person_name;
            """.format(columns=PEOPLE_COLUMNS), (user_id,))

            return cursor.fetchall()
    finally:
        conn.close()


def get_person_by_id(person_id):
    """Get a single person by ID."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT {columns}
                FROM people
                WHERE person_id = %s;
            """.format(columns=PEOPLE_COLUMNS), (person_id,))

            return cursor.fetchone()
    finally:
        conn.close()


def update_person(person_id, person_name):
    """Update a person's name."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE people
                SET person_name = %s
                WHERE person_id = %s
                RETURNING {columns};
            """.format(columns=PEOPLE_COLUMNS), (person_name, person_id))

            person = cursor.fetchone()

        conn.commit()
        return person

    finally:
        conn.close()


def delete_person(person_id):
    """Delete a person. Sets person_id to NULL in image_faces (ON DELETE SET NULL)."""
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM people
                WHERE person_id = %s
                RETURNING {columns};
            """.format(columns=PEOPLE_COLUMNS), (person_id,))

            person = cursor.fetchone()

        conn.commit()
        return person

    finally:
        conn.close()


def get_person_images(person_id):
    """Get all images where this person appears."""
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
                    i.upload_date,
                    f.confidence
                FROM images i
                JOIN image_faces f ON i.image_id = f.image_id
                WHERE f.person_id = %s
                ORDER BY i.upload_date DESC;
            """, (person_id,))

            return cursor.fetchall()
    finally:
        conn.close()

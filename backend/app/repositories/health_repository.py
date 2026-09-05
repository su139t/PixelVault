from app.db import get_db_connection


def get_database_details():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    current_database(),
                    current_user,
                    version();
            """)
            return cursor.fetchone()
    finally:
        conn.close()

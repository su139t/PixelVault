from app.db import get_db_connection


def search_images(user_id, query="", upload_date=None):
    """
    Perform a search for images based on a text query.
    Searches across: title, description, ai_description, detected_text, tags, and people.
    """
    if not query.strip() and not upload_date:
        return []

    query_str = f"%{query.strip().lower()}%" if query.strip() else None
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We use ILIKE for basic text matching.
            # In a real production app with pgvector or just full GIN indexes,
            # this would use to_tsquery for better full-text search.
            cursor.execute("""
                SELECT DISTINCT
                    i.image_id,
                    i.user_id,
                    i.title,
                    i.description,
                    i.file_name,
                    i.mime_type,
                    i.width,
                    i.height,
                    i.file_size,
                    i.telegram_chat_id,
                    i.telegram_message_id,
                    i.ai_description,
                    i.detected_text,
                    i.album_id,
                    i.visibility,
                    i.upload_date,
                    i.updated_at
                FROM images i
                LEFT JOIN image_tags it ON i.image_id = it.image_id
                LEFT JOIN tags t ON it.tag_id = t.tag_id
                LEFT JOIN image_faces f ON i.image_id = f.image_id
                LEFT JOIN people p ON f.person_id = p.person_id
                WHERE i.user_id = %s
                AND (%s::text IS NULL OR (
                    LOWER(i.title) LIKE %s OR
                    LOWER(i.description) LIKE %s OR
                    LOWER(i.file_name) LIKE %s OR
                    LOWER(i.ai_description) LIKE %s OR
                    LOWER(i.detected_text) LIKE %s OR
                    LOWER(t.tag_name) LIKE %s OR
                    LOWER(p.person_name) LIKE %s
                ))
                AND (%s::date IS NULL OR i.upload_date::date = %s::date)
                ORDER BY i.upload_date DESC;
            """, (
                user_id,
                query_str,
                query_str, query_str, query_str, query_str,
                query_str, query_str, query_str,
                upload_date, upload_date
            ))
            
            return cursor.fetchall()
    finally:
        conn.close()

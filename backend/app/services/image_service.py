import os
import uuid
import json
import logging
from io import BytesIO

from app.repositories.image_repository import (
    create_image_record,
    get_all_images as repo_get_all_images,
    get_image_by_id as repo_get_image_by_id,
    update_image as repo_update_image,
    delete_image as repo_delete_image,
    add_face_to_image
)
from app.repositories.people_repository import (
    get_all_people,
    create_person
)
from app.services.telegram_service import (
    upload_to_saved_messages_for_user as telegram_upload,
    download_media_for_user,
    delete_message_for_user
)
from app.services.pillow_service import (
    validate_image,
    remove_exif_and_compress,
    generate_thumbnail
)
from app.services.ollama_service import OllamaServiceError, generate_image_metadata
from app.services.compreface_service import recognize_faces


logger = logging.getLogger(__name__)


async def upload_image(user_id, file, title=None):
    """Process and upload an image, apply AI analysis, and save to DB."""
    # 1. Validate and get info
    info = validate_image(file)
    
    # 2. Process image (remove EXIF, compress)
    processed_image = remove_exif_and_compress(file)
    
    # Read bytes for AI processing before passing to Telegram (which consumes the stream)
    processed_image.seek(0)
    image_bytes = processed_image.read()
    processed_image.seek(0)
    
    unique_id = uuid.uuid4().hex

    # 3. Upload to Telegram
    processed_image.name = file.filename or f"{unique_id}.jpg"
    result = await telegram_upload(
        user_id,
        processed_image,
        caption=f"pixelvault:{unique_id}"
    )
    
    # 4. Save Telegram metadata first so AI availability cannot lose an upload.
    image_record = create_image_record(
        user_id=user_id,
        title=title,
        telegram_chat_id=result["telegram_chat_id"],
        telegram_message_id=result["telegram_message_id"],
        file_name=file.filename,
        mime_type=file.mimetype or "image/jpeg",
        width=info["width"],
        height=info["height"],
        file_size=info["file_size"],
        unique_id=unique_id,
    )
    
    image_id = image_record[0]
    
    # 5. Analyze asynchronously from the upload's perspective; failed AI does
    # not roll back the Telegram upload or image metadata.
    try:
        ai_meta = generate_image_metadata(image_bytes)
        from app.db import get_db_connection
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE images
                    SET ai_description = %s, detected_text = %s
                    WHERE image_id = %s
                """, (ai_meta["ai_description"], ai_meta["detected_text"], image_id))
            conn.commit()
        finally:
            conn.close()
    except OllamaServiceError as error:
        logger.warning("Ollama analysis pending for image %s: %s", image_id, error)

    # 7. Face Recognition (CompreFace)
    faces = recognize_faces(image_bytes)
    if faces:
        # Get existing people to avoid duplicates
        existing_people = get_all_people(user_id)
        people_map = {p[2].lower(): p[0] for p in existing_people} # name to id
        
        for face in faces:
            subject = face.get("subject")
            if not subject:
                continue
                
            confidence = face.get("confidence", 0.0)
            box = face.get("box", {})
            
            # Find or create person
            person_name = subject.strip()
            person_name_lower = person_name.lower()
            
            if person_name_lower in people_map:
                person_id = people_map[person_name_lower]
            else:
                new_person = create_person(user_id, person_name)
                person_id = new_person[0]
                people_map[person_name_lower] = person_id
                
            # Link face to image
            add_face_to_image(image_id, person_id, json.dumps(box), confidence)

    return image_record



def get_images(user_id):
    """Get all images for a user."""
    return repo_get_all_images(user_id)


def get_image(image_id):
    """Get a single image."""
    image = repo_get_image_by_id(image_id)
    if not image:
        raise ValueError(f"Image with id {image_id} not found")
    return image


async def get_image_file(image_id):
    """Download image bytes from Telegram."""
    image = get_image(image_id)
    
    # Extract telegram credentials from the tuple (assumes index 8, 9 based on our IMAGE_COLUMNS)
    # The columns: image_id(0), user_id(1), title(2), description(3), file_name(4), 
    # mime_type(5), width(6), height(7), file_size(8), telegram_chat_id(9), telegram_message_id(10)...
    # Wait, let's just get it safely
    chat_id = image[9]
    msg_id = image[10]
    
    return await download_media_for_user(image[1], chat_id, msg_id)


def update_image(image_id, title=None, description=None, visibility=None, album_id=None):
    """Update image metadata."""
    existing = repo_get_image_by_id(image_id)
    if not existing:
        raise ValueError(f"Image with id {image_id} not found")
        
    return repo_update_image(
        image_id, 
        title=title, 
        description=description, 
        visibility=visibility, 
        album_id=album_id
    )


async def delete_image(image_id):
    """Delete image from DB and Telegram."""
    existing = repo_get_image_by_id(image_id)
    if not existing:
        raise ValueError(f"Image with id {image_id} not found")
        
    chat_id = existing[9]
    msg_id = existing[10]
    
    # 1. Delete from Telegram
    try:
        await delete_message_for_user(existing[1], chat_id, msg_id)
    except Exception as e:
        # We might want to log this but still delete from DB
        print(f"Failed to delete from Telegram: {e}")
        
    # 2. Delete from DB
    return repo_delete_image(image_id)


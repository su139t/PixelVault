import asyncio
from flask import request, jsonify, send_file
import io

from app.services.image_service import (
    upload_image,
    get_images,
    get_image,
    get_image_file,
    update_image,
    delete_image
)
from app.utils.responses import error_response, success_response
from app.controllers.album_controller import serialize_image


def image_controller():
    """Handle POST /api/images"""
    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        return error_response("Image file is required", 400)

    user_id = request.form.get("user_id")
    if not user_id:
        return error_response("user_id is required", 400)

    try:
        image_record = asyncio.run(upload_image(
            user_id=int(user_id),
            file=uploaded_file,
            title=request.form.get("title"),
        ))
    except ValueError as exc:
        return error_response(str(exc), 400)

    return success_response(
        data={"image": serialize_image(image_record)},
        message="Image uploaded successfully",
        status_code=201,
    )


def get_images_controller():
    """Handle GET /api/images?user_id="""
    user_id = request.args.get("user_id")
    if not user_id:
        return error_response("user_id query parameter is required", 400)
        
    images = get_images(int(user_id))
    
    return success_response(
        data={"images": [serialize_image(img) for img in images]}
    )


def get_image_by_id_controller(image_id):
    """Handle GET /api/images/<id>"""
    try:
        image = get_image(image_id)
        return success_response(
            data={"image": serialize_image(image)}
        )
    except ValueError as e:
        return error_response(str(e), 404)


def get_image_file_controller(image_id):
    """Handle GET /api/images/<id>/file"""
    try:
        # Get DB record first to get mime_type
        image = get_image(image_id)
        mime_type = image[5] or "image/jpeg"
        file_name = image[4] or f"image_{image_id}.jpg"
        
        # Download from Telegram
        file_bytes = asyncio.run(get_image_file(image_id))
        
        return send_file(
            file_bytes,
            mimetype=mime_type,
            as_attachment=False,
            download_name=file_name
        )
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        print(f"Error downloading image: {e}")
        return error_response("Failed to retrieve image file", 500)


def update_image_controller(image_id):
    """Handle PUT /api/images/<id>"""
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)
        
    try:
        image = update_image(
            image_id,
            title=data.get("title"),
            description=data.get("description"),
            visibility=data.get("visibility"),
            album_id=data.get("album_id")
        )
        return success_response(
            data={"image": serialize_image(image)},
            message="Image updated successfully"
        )
    except ValueError as e:
        return error_response(str(e), 404)


def delete_image_controller(image_id):
    """Handle DELETE /api/images/<id>"""
    try:
        asyncio.run(delete_image(image_id))
        # Note: deleted only contains telegram_chat_id, telegram_message_id as per our repo code
        return success_response(
            message="Image deleted successfully"
        )
    except ValueError as e:
        return error_response(str(e), 404)


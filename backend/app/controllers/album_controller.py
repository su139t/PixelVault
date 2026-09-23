from flask import jsonify, request

from app.services.album_service import (
    create_album,
    get_all_albums,
    get_album_by_id,
    update_album,
    delete_album,
    add_image_to_album,
    remove_image_from_album,
    get_album_images
)
from app.utils.responses import success_response


def create_album_controller():
    """Handle POST /api/albums"""
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    # For now, use user_id from request body
    # Later will come from auth token
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id is required"
        }), 400

    album = create_album(
        user_id=int(user_id),
        album_name=data.get("album_name")
    )

    return success_response(
        data={"album": serialize_album(album)},
        message="Album created successfully",
        status_code=201
    )


def get_albums_controller():
    """Handle GET /api/albums?user_id="""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id query parameter is required"
        }), 400

    albums = get_all_albums(int(user_id))

    return success_response(
        data={"albums": [serialize_album(a) for a in albums]}
    )


def get_album_by_id_controller(album_id):
    """Handle GET /api/albums/<id>"""
    album = get_album_by_id(album_id)

    return success_response(
        data={"album": serialize_album(album)}
    )


def update_album_controller(album_id):
    """Handle PUT /api/albums/<id>"""
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    album = update_album(
        album_id,
        album_name=data.get("album_name")
    )

    return success_response(
        data={"album": serialize_album(album)},
        message="Album updated successfully"
    )


def delete_album_controller(album_id):
    """Handle DELETE /api/albums/<id>"""
    deleted = delete_album(album_id)

    return success_response(
        data={"album": serialize_album(deleted)},
        message="Album deleted successfully"
    )


def add_image_to_album_controller(album_id, image_id):
    """Handle POST /api/albums/<id>/images/<image_id>"""
    add_image_to_album(album_id, image_id)

    return success_response(
        message="Image added to album successfully"
    )


def remove_image_from_album_controller(album_id, image_id):
    """Handle DELETE /api/albums/<id>/images/<image_id>"""
    remove_image_from_album(album_id, image_id)

    return success_response(
        message="Image removed from album successfully"
    )


def get_album_images_controller(album_id):
    """Handle GET /api/albums/<id>/images"""
    images = get_album_images(album_id)

    return success_response(
        data={"images": [serialize_image(img) for img in images]}
    )


def serialize_album(album):
    return {
        "album_id": album[0],
        "user_id": album[1],
        "album_name": album[2],
        "created_at": serialize_datetime(album[3])
    }


def serialize_datetime(value):
    if not value:
        return None
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def serialize_image(image):
    return {
        "image_id": image[0],
        "user_id": image[1],
        "title": image[2],
        "description": image[3],
        "file_name": image[4],
        "mime_type": image[5],
        "width": image[6],
        "height": image[7],
        "file_size": image[8],
        "telegram_chat_id": image[9],
        "telegram_message_id": image[10],
        "ai_description": image[11],
        "detected_text": image[12],
        "album_id": image[13],
        "visibility": image[14],
        "upload_date": serialize_datetime(image[15]),
        "updated_at": serialize_datetime(image[16]),
    }

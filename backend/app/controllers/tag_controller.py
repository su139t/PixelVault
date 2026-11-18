from flask import jsonify, request

from app.services.tag_service import (
    create_tag,
    get_all_tags,
    delete_tag,
    add_tag_to_image,
    remove_tag_from_image,
    get_tags_for_image
)
from app.utils.responses import success_response


def create_tag_controller():
    """Handle POST /api/tags"""
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    user_id = data.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id is required"
        }), 400

    tag = create_tag(
        user_id=int(user_id),
        tag_name=data.get("tag_name")
    )

    return success_response(
        data={"tag": serialize_tag(tag)},
        message="Tag created successfully",
        status_code=201
    )


def get_tags_controller():
    """Handle GET /api/tags?user_id="""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id query parameter is required"
        }), 400

    tags = get_all_tags(int(user_id))

    return success_response(
        data={"tags": [serialize_tag(t) for t in tags]}
    )


def delete_tag_controller(tag_id):
    """Handle DELETE /api/tags/<id>"""
    deleted = delete_tag(tag_id)

    return success_response(
        data={"tag": serialize_tag(deleted)},
        message="Tag deleted successfully"
    )


def add_tag_to_image_controller(image_id, tag_id):
    """Handle POST /api/images/<id>/tags/<tag_id>"""
    add_tag_to_image(image_id, tag_id)

    return success_response(
        message="Tag added to image successfully"
    )


def remove_tag_from_image_controller(image_id, tag_id):
    """Handle DELETE /api/images/<id>/tags/<tag_id>"""
    remove_tag_from_image(image_id, tag_id)

    return success_response(
        message="Tag removed from image successfully"
    )


def get_image_tags_controller(image_id):
    """Handle GET /api/images/<id>/tags"""
    tags = get_tags_for_image(image_id)

    return success_response(
        data={"tags": [serialize_tag(t) for t in tags]}
    )


def serialize_tag(tag):
    return {
        "tag_id": tag[0],
        "user_id": tag[1],
        "tag_name": tag[2],
        "created_at": tag[3].isoformat() if tag[3] else None
    }

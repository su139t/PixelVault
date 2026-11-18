from flask import jsonify, request

from app.services.favorite_service import (
    add_favorite,
    remove_favorite,
    get_user_favorites
)
from app.utils.responses import success_response
# Using the serializer from album_controller to avoid duplication
# In a real app we'd move this to a shared serializers.py
from app.controllers.album_controller import serialize_image


def add_favorite_controller(image_id):
    """Handle POST /api/images/<id>/favorite"""
    data = request.get_json() or {}
    
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id is required"
        }), 400

    favorite = add_favorite(int(user_id), image_id)

    return success_response(
        message="Image added to favorites successfully"
    )


def remove_favorite_controller(image_id):
    """Handle DELETE /api/images/<id>/favorite"""
    # Assuming user_id is passed as query param for DELETE
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id query parameter is required"
        }), 400

    remove_favorite(int(user_id), image_id)

    return success_response(
        message="Image removed from favorites successfully"
    )


def get_favorites_controller():
    """Handle GET /api/favorites?user_id="""
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id query parameter is required"
        }), 400

    images = get_user_favorites(int(user_id))

    return success_response(
        data={"favorites": [serialize_image(img) for img in images]}
    )

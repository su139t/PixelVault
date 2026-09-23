from flask import jsonify, request

from app.services.search_service import search_images
from app.utils.responses import success_response, error_response
from app.controllers.album_controller import serialize_image


def search_controller():
    """Handle GET /api/search?q=&user_id="""
    query = request.args.get("q", "")
    upload_date = request.args.get("date")
    user_id = request.args.get("user_id")
    
    if not user_id:
        return error_response("user_id query parameter is required", 400)
        
    if not query and not upload_date:
        return success_response(data={"images": []})
        
    images = search_images(int(user_id), query, upload_date)
    
    return success_response(
        data={"images": [serialize_image(img) for img in images]}
    )

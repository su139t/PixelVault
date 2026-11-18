from flask import Blueprint

from app.controllers.favorite_controller import (
    add_favorite_controller,
    remove_favorite_controller,
    get_favorites_controller
)


favorite_bp = Blueprint(
    "favorites",
    __name__
)

# Note: The add/remove favorite routes are better placed on the images 
# blueprint (/api/images/<id>/favorite), but we can define the global 
# favorites list route here.

@favorite_bp.get("")
def get_favorites():
    return get_favorites_controller()

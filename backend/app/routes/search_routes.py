from flask import Blueprint

from app.controllers.search_controller import search_controller


search_bp = Blueprint(
    "search",
    __name__
)


@search_bp.get("")
def search():
    return search_controller()

from flask import Blueprint

from app.controllers.album_controller import (
    create_album_controller,
    get_albums_controller,
    get_album_by_id_controller,
    update_album_controller,
    delete_album_controller,
    add_image_to_album_controller,
    remove_image_from_album_controller,
    get_album_images_controller
)


album_bp = Blueprint(
    "albums",
    __name__
)


@album_bp.post("")
def create_album():
    return create_album_controller()


@album_bp.get("")
def get_albums():
    return get_albums_controller()


@album_bp.get("/<int:album_id>")
def get_album(album_id):
    return get_album_by_id_controller(album_id)


@album_bp.put("/<int:album_id>")
def update_album(album_id):
    return update_album_controller(album_id)


@album_bp.delete("/<int:album_id>")
def delete_album(album_id):
    return delete_album_controller(album_id)


@album_bp.post("/<int:album_id>/images/<int:image_id>")
def add_image(album_id, image_id):
    return add_image_to_album_controller(album_id, image_id)


@album_bp.delete("/<int:album_id>/images/<int:image_id>")
def remove_image(album_id, image_id):
    return remove_image_from_album_controller(album_id, image_id)


@album_bp.get("/<int:album_id>/images")
def get_images(album_id):
    return get_album_images_controller(album_id)

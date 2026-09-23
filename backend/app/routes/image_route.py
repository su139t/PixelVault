from flask import Blueprint

from app.controllers.image_controller import (
    image_controller,
    get_images_controller,
    get_image_by_id_controller,
    get_image_file_controller,
    update_image_controller,
    delete_image_controller
)
from app.controllers.tag_controller import (
    add_tag_to_image_controller,
    remove_tag_from_image_controller,
    get_image_tags_controller
)
from app.controllers.favorite_controller import (
    add_favorite_controller,
    remove_favorite_controller
)


image_bp = Blueprint("images", __name__)


@image_bp.post("")
def upload_image():
    return image_controller()


@image_bp.get("")
def get_images():
    return get_images_controller()


@image_bp.get("/<int:image_id>")
def get_image(image_id):
    return get_image_by_id_controller(image_id)


@image_bp.get("/<int:image_id>/file")
def get_image_file(image_id):
    return get_image_file_controller(image_id)


@image_bp.put("/<int:image_id>")
def update_image(image_id):
    return update_image_controller(image_id)


@image_bp.delete("/<int:image_id>")
def delete_image(image_id):
    return delete_image_controller(image_id)


# --- Image-Tag association routes ---

@image_bp.post("/<int:image_id>/tags/<int:tag_id>")
def add_tag(image_id, tag_id):
    return add_tag_to_image_controller(image_id, tag_id)


@image_bp.delete("/<int:image_id>/tags/<int:tag_id>")
def remove_tag(image_id, tag_id):
    return remove_tag_from_image_controller(image_id, tag_id)


@image_bp.get("/<int:image_id>/tags")
def get_tags(image_id):
    return get_image_tags_controller(image_id)


# --- Image-Favorite association routes ---

@image_bp.post("/<int:image_id>/favorite")
def add_favorite(image_id):
    return add_favorite_controller(image_id)


@image_bp.delete("/<int:image_id>/favorite")
def remove_favorite(image_id):
    return remove_favorite_controller(image_id)


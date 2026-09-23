from flask import Blueprint

from app.controllers.tag_controller import (
    create_tag_controller,
    get_tags_controller,
    delete_tag_controller,
    add_tag_to_image_controller,
    remove_tag_from_image_controller,
    get_image_tags_controller
)


tag_bp = Blueprint(
    "tags",
    __name__
)


@tag_bp.post("")
def create_tag():
    return create_tag_controller()


@tag_bp.get("")
def get_tags():
    return get_tags_controller()


@tag_bp.delete("/<int:tag_id>")
def delete_tag(tag_id):
    return delete_tag_controller(tag_id)


# Image-tag routes are registered on the images blueprint
# but we keep them here for tag module cohesion.
# They will be registered under /api/tags prefix.

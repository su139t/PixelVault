from flask import Blueprint

from app.controllers.people_controller import (
    create_person_controller,
    get_people_controller,
    get_person_by_id_controller,
    update_person_controller,
    delete_person_controller,
    get_person_images_controller
)


people_bp = Blueprint(
    "people",
    __name__
)


@people_bp.post("")
def create_person():
    return create_person_controller()


@people_bp.get("")
def get_people():
    return get_people_controller()


@people_bp.get("/<int:person_id>")
def get_person(person_id):
    return get_person_by_id_controller(person_id)


@people_bp.put("/<int:person_id>")
def update_person(person_id):
    return update_person_controller(person_id)


@people_bp.delete("/<int:person_id>")
def delete_person(person_id):
    return delete_person_controller(person_id)


@people_bp.get("/<int:person_id>/images")
def get_images(person_id):
    return get_person_images_controller(person_id)

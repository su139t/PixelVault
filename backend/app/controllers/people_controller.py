from flask import jsonify, request

from app.services.people_service import (
    create_person,
    get_all_people,
    get_person_by_id,
    update_person,
    delete_person,
    get_person_images
)
from app.utils.responses import success_response
from app.controllers.album_controller import serialize_image


def create_person_controller():
    """Handle POST /api/people"""
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

    person = create_person(
        user_id=int(user_id),
        person_name=data.get("person_name"),
        compreface_subject_id=data.get("compreface_subject_id")
    )

    return success_response(
        data={"person": serialize_person(person)},
        message="Person created successfully",
        status_code=201
    )


def get_people_controller():
    """Handle GET /api/people?user_id="""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id query parameter is required"
        }), 400

    people = get_all_people(int(user_id))

    return success_response(
        data={"people": [serialize_person(p) for p in people]}
    )


def get_person_by_id_controller(person_id):
    """Handle GET /api/people/<id>"""
    person = get_person_by_id(person_id)

    return success_response(
        data={"person": serialize_person(person)}
    )


def update_person_controller(person_id):
    """Handle PUT /api/people/<id>"""
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    person = update_person(
        person_id,
        person_name=data.get("person_name")
    )

    return success_response(
        data={"person": serialize_person(person)},
        message="Person updated successfully"
    )


def delete_person_controller(person_id):
    """Handle DELETE /api/people/<id>"""
    deleted = delete_person(person_id)

    return success_response(
        data={"person": serialize_person(deleted)},
        message="Person deleted successfully"
    )


def get_person_images_controller(person_id):
    """Handle GET /api/people/<id>/images"""
    images = get_person_images(person_id)

    # Note: image tuples here include 'confidence' at index 14
    serialized_images = []
    for img in images:
        s_img = serialize_image(img)
        s_img["confidence"] = float(img[14]) if img[14] else None
        serialized_images.append(s_img)

    return success_response(
        data={"images": serialized_images}
    )


def serialize_person(person):
    return {
        "person_id": person[0],
        "user_id": person[1],
        "person_name": person[2],
        "compreface_subject_id": person[3],
        "created_at": person[4].isoformat() if person[4] else None
    }

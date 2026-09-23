from app.repositories.people_repository import (
    create_person as repo_create_person,
    get_all_people as repo_get_all_people,
    get_person_by_id as repo_get_person_by_id,
    update_person as repo_update_person,
    delete_person as repo_delete_person,
    get_person_images as repo_get_person_images
)


def create_person(user_id, person_name, compreface_subject_id=None):
    """Create a new person."""
    if not person_name or not person_name.strip():
        raise ValueError("Person name is required")

    return repo_create_person(user_id, person_name.strip(), compreface_subject_id)


def get_all_people(user_id):
    """Get all people for a user."""
    return repo_get_all_people(user_id)


def get_person_by_id(person_id):
    """Get a single person."""
    person = repo_get_person_by_id(person_id)

    if not person:
        raise ValueError(f"Person with id {person_id} not found")

    return person


def update_person(person_id, person_name):
    """Update a person's name."""
    if not person_name or not person_name.strip():
        raise ValueError("Person name is required")

    existing = repo_get_person_by_id(person_id)
    if not existing:
        raise ValueError(f"Person with id {person_id} not found")

    return repo_update_person(person_id, person_name.strip())


def delete_person(person_id):
    """Delete a person."""
    deleted = repo_delete_person(person_id)

    if not deleted:
        raise ValueError(f"Person with id {person_id} not found")

    return deleted


def get_person_images(person_id):
    """Get all images where this person appears."""
    # Verify person exists
    existing = repo_get_person_by_id(person_id)
    if not existing:
        raise ValueError(f"Person with id {person_id} not found")

    return repo_get_person_images(person_id)

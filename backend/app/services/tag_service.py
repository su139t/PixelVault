from app.repositories.tag_repository import (
    create_tag as repo_create_tag,
    get_all_tags as repo_get_all_tags,
    get_tag_by_id as repo_get_tag_by_id,
    delete_tag as repo_delete_tag,
    add_tag_to_image as repo_add_tag_to_image,
    remove_tag_from_image as repo_remove_tag_from_image,
    get_tags_for_image as repo_get_tags_for_image
)


def create_tag(user_id, tag_name):
    """Create a new tag."""
    if not tag_name or not tag_name.strip():
        raise ValueError("Tag name is required")

    return repo_create_tag(user_id, tag_name.strip().lower())


def get_all_tags(user_id):
    """Get all tags for a user."""
    return repo_get_all_tags(user_id)


def delete_tag(tag_id):
    """Delete a tag."""
    deleted = repo_delete_tag(tag_id)

    if not deleted:
        raise ValueError(f"Tag with id {tag_id} not found")

    return deleted


def add_tag_to_image(image_id, tag_id):
    """Add a tag to an image."""
    # Verify tag exists
    tag = repo_get_tag_by_id(tag_id)
    if not tag:
        raise ValueError(f"Tag with id {tag_id} not found")

    repo_add_tag_to_image(image_id, tag_id)


def remove_tag_from_image(image_id, tag_id):
    """Remove a tag from an image."""
    result = repo_remove_tag_from_image(image_id, tag_id)

    if not result:
        raise ValueError(
            f"Tag {tag_id} is not associated with image {image_id}"
        )


def get_tags_for_image(image_id):
    """Get all tags for an image."""
    return repo_get_tags_for_image(image_id)

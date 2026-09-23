from app.repositories.album_repository import (
    create_album as repo_create_album,
    get_all_albums as repo_get_all_albums,
    get_album_by_id as repo_get_album_by_id,
    update_album as repo_update_album,
    delete_album as repo_delete_album,
    add_image_to_album as repo_add_image,
    remove_image_from_album as repo_remove_image,
    get_album_images as repo_get_album_images
)


def create_album(user_id, album_name):
    """Create a new album for the user."""
    if not album_name or not album_name.strip():
        raise ValueError("Album name is required")

    return repo_create_album(user_id, album_name.strip())


def get_all_albums(user_id):
    """Get all albums for a user."""
    return repo_get_all_albums(user_id)


def get_album_by_id(album_id):
    """Get a single album. Raises ValueError if not found."""
    album = repo_get_album_by_id(album_id)

    if not album:
        raise ValueError(f"Album with id {album_id} not found")

    return album


def update_album(album_id, album_name):
    """Rename an album. Raises ValueError if not found."""
    if not album_name or not album_name.strip():
        raise ValueError("Album name is required")

    existing = repo_get_album_by_id(album_id)
    if not existing:
        raise ValueError(f"Album with id {album_id} not found")

    return repo_update_album(album_id, album_name.strip())


def delete_album(album_id):
    """Delete an album. Raises ValueError if not found."""
    deleted = repo_delete_album(album_id)

    if not deleted:
        raise ValueError(f"Album with id {album_id} not found")

    return deleted


def add_image_to_album(album_id, image_id):
    """Add an image to an album."""
    # Verify album exists
    album = repo_get_album_by_id(album_id)
    if not album:
        raise ValueError(f"Album with id {album_id} not found")

    result = repo_add_image(album_id, image_id)
    if not result:
        raise ValueError(f"Image with id {image_id} not found")

    return result


def remove_image_from_album(album_id, image_id):
    """Remove an image from an album."""
    result = repo_remove_image(album_id, image_id)

    if not result:
        raise ValueError(
            f"Image {image_id} is not in album {album_id}"
        )

    return result


def get_album_images(album_id):
    """Get all images in an album."""
    # Verify album exists
    album = repo_get_album_by_id(album_id)
    if not album:
        raise ValueError(f"Album with id {album_id} not found")

    return repo_get_album_images(album_id)

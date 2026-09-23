from app.repositories.favorite_repository import (
    add_favorite as repo_add_favorite,
    remove_favorite as repo_remove_favorite,
    get_user_favorites as repo_get_user_favorites
)
from app.repositories.image_repository import get_image_by_id


def add_favorite(user_id, image_id):
    """Add an image to favorites."""
    # Note: in a real implementation we should verify the user_id exists, 
    # but the foreign key constraint will catch it at the DB level.
    
    # We could check if the image exists, but ON CONFLICT and foreign key
    # will handle invalid image_ids safely.
    
    return repo_add_favorite(user_id, image_id)


def remove_favorite(user_id, image_id):
    """Remove an image from favorites."""
    result = repo_remove_favorite(user_id, image_id)
    
    if not result:
        raise ValueError("Favorite not found")
        
    return result


def get_user_favorites(user_id):
    """Get all favorite images for a user."""
    return repo_get_user_favorites(user_id)

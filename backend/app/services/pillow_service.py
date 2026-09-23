from PIL import Image
from io import BytesIO


def validate_image(file_storage):
    if file_storage is None:
        raise ValueError("Image file is required")

    image = Image.open(file_storage)
    image.verify()

    file_storage.seek(0)
    image = Image.open(file_storage)

    width, height = image.size
    format_name = image.format or "UNKNOWN"

    return {
        "width": width,
        "height": height,
        "format": format_name,
        "file_size": len(file_storage.read()),
    }


def remove_exif_and_compress(file_storage, quality=85):
    """
    Remove EXIF data (including GPS) and compress the image.
    Returns a BytesIO object with the processed image.
    """
    file_storage.seek(0)
    image = Image.open(file_storage)
    
    # Convert to RGB to safely save as JPEG
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    # Get original EXIF if needed for rotation (skip for now to keep it simple, 
    # but normally we'd apply EXIF rotation before stripping)
    
    # Strip EXIF by simply not passing it to save()
    output = BytesIO()
    image.save(output, format="JPEG", quality=quality, optimize=True)
    output.seek(0)
    
    return output


def generate_thumbnail(file_storage, max_size=(400, 400)):
    """
    Generate a thumbnail for the given image.
    Returns a BytesIO object.
    """
    file_storage.seek(0)
    image = Image.open(file_storage)
    
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = BytesIO()
    image.save(output, format="JPEG", quality=80, optimize=True)
    output.seek(0)
    
    return output


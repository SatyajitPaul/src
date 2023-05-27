import os
import uuid
from PIL import Image
from fastapi import HTTPException, status, UploadFile

UPLOAD_DIR = "uploads"
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


def save_image(file: UploadFile) -> str:
    
    # Check if the image size exceeds the limit
    if file.content_length > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image size exceeds the limit")


    # Create a unique filename using UUID
    unique_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Create the directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the image file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Resize the image if needed (optional)
    resized_image = resize_image(file_path, (800, 600))
    resized_image.save(file_path)

    return file_path


def resize_image(file_path: str, size: tuple) -> Image.Image:
    # Open the image using Pillow
    image = Image.open(file_path)

    # Resize the image while maintaining aspect ratio
    image.thumbnail(size)

    return image

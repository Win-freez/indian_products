import uuid
import re
from pathlib import Path

from fastapi import HTTPException, UploadFile


def generate_safe_filename(file: UploadFile) -> str:
    try:
        ext = Path(file.filename).suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(400, "Invalid file type")

        new_filename = f"{uuid.uuid4()}"

        return new_filename
    except Exception as e:
        raise HTTPException(500, f"Error uploading file: {str(e)}")

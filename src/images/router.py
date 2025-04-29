import shutil
import aiofiles
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends

from src.config import BASE_DIR
from src.images.utils import generate_safe_filename
from src.users.models import User
from src.users.dependencies import check_user_is_admin

router = APIRouter(prefix="/images", tags=["Загрузка картинки"])


@router.post("/products")
async def add_product_img(user: Annotated[User, Depends(check_user_is_admin)],
                          file: UploadFile = File(...)):
    image_name = generate_safe_filename(file)
    file_path = BASE_DIR / "src" / "static" / "images" / f"{image_name}.webp"

    async with aiofiles.open(file_path, "wb+") as buffer:
        await buffer.write(await file.read())

    return {
        "status": "success",
        "filename": f"{image_name}.webp",
        "path": str(file_path.relative_to(BASE_DIR))
    }

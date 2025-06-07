from os.path import exists
from constants import Directories
from exceptions import NotFoundException
from fastapi.responses import FileResponse
from utils import generate_file_path, generate_file_media_type


async def get_photo_by_slug(slug: str) -> FileResponse:
    path = generate_file_path(slug, Directories.PHOTOS)

    if not exists(path):
        raise NotFoundException(message="Photo not found")

    media_type = generate_file_media_type(path)

    return FileResponse(path=path, media_type=media_type)

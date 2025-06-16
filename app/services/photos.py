from os.path import join, exists
from mimetypes import guess_type
from settings import get_settings
from constants import Directories
from exceptions import NotFoundException
from fastapi.responses import FileResponse


settings = get_settings()


async def get_photo_by_slug(slug: str) -> FileResponse:
    path = join(settings.directory_path, Directories.PHOTOS.value, slug)

    if not exists(path):
        raise NotFoundException(message="Photo not found")

    media_type = guess_type(path)[0] or "text/plain"

    return FileResponse(path=path, media_type=media_type)

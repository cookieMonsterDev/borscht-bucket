from os.path import join, exists
from mimetypes import guess_type
from settings import get_settings
from constants import Directories
from exceptions import NotFoundException
from fastapi.responses import FileResponse


settings = get_settings()


async def get_document_by_slug(slug: str) -> FileResponse:
    path = join(settings.directory_path, Directories.DOCUMENTS.value, slug)

    if not exists(path):
        raise NotFoundException(message="Document not found")

    media_type = guess_type(path)[0] or "text/plain"

    headers = {"Content-Disposition": f"attachment; filename={slug}"}

    return FileResponse(path=path, media_type=media_type, headers=headers, filename=slug)

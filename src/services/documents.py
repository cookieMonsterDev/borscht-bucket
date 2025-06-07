from os.path import exists
from constants import Directories
from exceptions import NotFoundException
from fastapi.responses import FileResponse
from utils import generate_file_path, generate_file_media_type


async def get_document_by_slug(slug: str) -> FileResponse:
    path = generate_file_path(slug, Directories.DOCUMENTS)

    if not exists(path):
        raise NotFoundException(message="Document not found")

    media_type = generate_file_media_type(path)

    headers = {"Content-Disposition": f"attachment; filename={slug}"}

    return FileResponse(path=path, media_type=media_type, headers=headers, filename=slug)

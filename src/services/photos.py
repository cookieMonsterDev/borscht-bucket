from mimetypes import guess_type
from fastapi.responses import FileResponse
from utils import generate_file_path, validate_file_existence, Directories


async def get_photo_by_slug(document_slug: str) -> FileResponse:
    path = generate_file_path(document_slug, Directories.PHOTOS)

    validate_file_existence(document_slug)

    media_type = guess_type(path)[0] or "application/octet-stream"
    headers = {"Content-Disposition": f"attachment; filename={document_slug}"}

    return FileResponse(path=path, media_type=media_type, headers=headers, filename=document_slug)

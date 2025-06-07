from os.path import exists
from constants import Directories
from exceptions import NotFoundException
from fastapi.responses import StreamingResponse
from utils import generate_file_path, generate_file_media_type


async def get_video_by_slug(slug: str) -> StreamingResponse:
    path = generate_file_path(slug, Directories.VIDEOS)

    if not exists(path):
        raise NotFoundException(message="Video not found")

    media_type = generate_file_media_type(path)

    return StreamingResponse(path=path, media_type=media_type)

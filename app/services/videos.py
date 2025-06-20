import aiofiles
from typing import Tuple
from mimetypes import guess_type
from constants import Directories
from settings import get_settings
from exceptions import NotFoundException
from os.path import join, exists, getsize
from fastapi.responses import StreamingResponse


settings = get_settings()


async def async_file_iterator(path: str, start: int, end: int):
    length = end - start + 1
    remaining = length
    chunk_size = settings.chunk_size

    async with aiofiles.open(path, "rb") as file:
        await file.seek(start)
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            data = await file.read(read_size)
            if not data:
                break
            yield data
            remaining -= len(data)


def parse_range_header(range_header: str, file_size: int) -> Tuple[int, int]:
    if not range_header or not range_header.startswith("bytes="):
        return 0, file_size - 1

    try:
        range_values = range_header.replace("bytes=", "").split("-")

        start = int(range_values[0]) if range_values[0] else 0

        end = int(range_values[1]) if len(range_values) > 1 and range_values[1] else file_size - 1

        start = max(0, min(start, file_size - 1))

        end = max(start, min(end, file_size - 1))

    except (ValueError, IndexError):
        start, end = 0, file_size - 1

    return start, end


async def get_video_by_slug(slug: str, range: str) -> StreamingResponse:
    path = join(settings.directory_path, Directories.VIDEOS.value, slug)

    if not exists(path):
        raise NotFoundException(message="Video not found")

    file_size = getsize(path)

    media_type = guess_type(path)[0] or "application/octet-stream"

    start, end = parse_range_header(range, file_size)

    content_length = end - start + 1

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": media_type,
        "Content-Length": str(content_length),
        "Content-Range": f"bytes {start}-{end}/{file_size}",
    }

    return StreamingResponse(
        content=async_file_iterator(path, start, end),
        status_code=206,
        headers=headers,
        media_type=media_type,
    )

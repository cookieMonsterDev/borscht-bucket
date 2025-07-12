from re import sub, UNICODE
from datetime import datetime
from shutil import copyfileobj
from fastapi import UploadFile
from os import makedirs, remove
from mimetypes import guess_type
from settings import get_settings
from fastapi.responses import JSONResponse
from .optimizer_state import optimizer_queue
from os.path import dirname, join, exists, splitext
from exceptions import HTTPException, NotFoundException
from constants import Directories, PhotoMediaTypes, VideoMediaTypes


settings = get_settings()


def generate_file_slug(filename: str) -> str:
    name, extension = splitext(filename)
    name = sub(r'[^\w\d]+', '-', name.lower(), flags=UNICODE).strip('-')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{name}-{timestamp}{extension}"


def generate_file_directory_type(filename: str) -> str:
    media_type = guess_type(filename)[0] or "text/plain"

    if media_type in [m.value for m in PhotoMediaTypes]:
        return Directories.PHOTOS.value

    if media_type in [m.value for m in VideoMediaTypes]:
        return Directories.VIDEOS.value

    return Directories.DOCUMENTS.value


def generate_file_url(directory: Directories, slug: str) -> str:
    return join(settings.host_path, directory, slug)


async def optimize_video(path: str) -> None:
    try:
        media_type = guess_type(path)[0] or ""

        if not media_type.startswith("video/"):
            return

        base, ext = splitext(path)

        temp_path = f"{base}-temp{ext}"

        result = run(
            ["ffmpeg", "-i", path, "-c", "copy", "-movflags", "+faststart", "-y", temp_path],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

        if not result.returncode:
            remove(path)
            run(["mv", temp_path, path])

    except OSError as error:
        print(f"Error optimizing video: {error}")


async def upload_file(file: UploadFile, background_tasks: BackgroundTasks) -> JSONResponse:
    slug = generate_file_slug(file.filename)

    directory = generate_file_directory_type(file.filename)

    path = join(settings.directory_path, directory, slug)

    makedirs(dirname(path), exist_ok=True)

    url = generate_file_url(directory, slug)

    try:
        with open(path, 'wb') as buffer:
            copyfileobj(file.file, buffer)

        optimizer_queue.put(path)

    except OSError as error:
        raise HTTPException(message=error.strerror)

    return JSONResponse({"message": "File uploaded successfully", "url": url}, status_code=201)


async def delete_file(directory: str, slug: str) -> JSONResponse:

    if directory not in Directories._value2member_map_:
        raise NotFoundException(message="File not found")

    path = join(settings.directory_path, Directories[directory.upper()].value, slug)

    if not exists(path):
        raise NotFoundException(message="File not found")

    remove(path)

    return JSONResponse({"message": "File deleted successfully"}, status_code=200)

from re import sub, UNICODE
from datetime import datetime
from fastapi import UploadFile
from shutil import copyfileobj
from os import makedirs, remove
from mimetypes import guess_type
from settings import get_settings
from os.path import dirname, join, exists
from fastapi.responses import JSONResponse
from exceptions import HTTPException, NotFoundException
from constants import Directories, PhotoMediaTypes, VideoMediaTypes


settings = get_settings()


def generate_file_slug(filename: str) -> str:
    (filename, extension) = filename.rsplit('.', 1)
    filename = sub(r'[^\w\d]+', '-', filename.lower(), flags=UNICODE).strip('-')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{filename}-{timestamp}.{extension}"


def generate_file_directory_type(filename: str) -> str:
    media_type = guess_type(filename)[0] or "text/plain"

    if media_type in PhotoMediaTypes._value2member_map_:
        return Directories.PHOTOS.value

    if media_type in VideoMediaTypes._value2member_map_:
        return Directories.VIDEOS.value

    return Directories.DOCUMENTS.value


def generate_file_url(directory: Directories, slug: str) -> str:
    return join(settings.host_path, directory, slug)


async def upload_file(file: UploadFile) -> JSONResponse:
    slug = generate_file_slug(file.filename)

    directory = generate_file_directory_type(file.filename)

    path = join(settings.directory_path, directory, slug)

    makedirs(dirname(path), exist_ok=True)

    url = generate_file_url(directory, slug)

    try:
        with open(path, 'wb') as buffer:
            copyfileobj(file.file, buffer)
    except OSError as error:
        raise HTTPException(message=error.strerror)

    return JSONResponse({"message": "File uploaded successfully", "url": url}, status_code=201)


async def delete_file(directory: str, slug: str) -> JSONResponse:

    if directory not in Directories._value2member_map_:
        raise NotFoundException(message="File not found")

    path = join(slug, Directories[directory.upper()].value)

    if not exists(path):
        raise NotFoundException(message="File not found")

    remove(path)

    return JSONResponse({"message": "File deleted successfully"}, status_code=200)

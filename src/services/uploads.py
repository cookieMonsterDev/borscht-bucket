from os import makedirs
from re import sub, UNICODE
from datetime import datetime
from fastapi import UploadFile
from shutil import copyfileobj
from settings import get_settings
from os.path import dirname, join
from exceptions import HTTPException
from fastapi.responses import JSONResponse
from constants import Directories, PhotoMediaTypes, VideoMediaTypes
from utils import generate_file_path, generate_file_media_type, Directories

settings = get_settings()


def generate_file_slug(filename: str) -> str:
    (filename, extension) = filename.rsplit('.', 1)
    filename = sub(r'[^\w\d]+', '-', filename.lower(), flags=UNICODE).strip('-')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{filename}-{timestamp}.{extension}"


def generate_file_directory_type(filename: str) -> Directories:
    media_type = generate_file_media_type(filename)

    if media_type in PhotoMediaTypes._value2member_map_:
        return Directories.PHOTOS

    if media_type in VideoMediaTypes._value2member_map_:
        return Directories.VIDEOS

    return Directories.DOCUMENTS


def generate_file_url(directory: Directories, slug: str) -> str:
    return join(settings.host_path, directory, slug)


async def upload_file(file: UploadFile) -> JSONResponse:
    slug = generate_file_slug(file.filename)

    directory = generate_file_directory_type(file.filename)

    path = generate_file_path(slug, directory)

    makedirs(dirname(path), exist_ok=True)

    url = generate_file_url(directory, slug)

    try:
        with open(path, 'wb') as buffer:
            copyfileobj(file.file, buffer)
    except OSError as error:
        raise HTTPException(message=error.strerror)

    return JSONResponse({"message": "File uploaded successfully", "url": url}, status_code=201)

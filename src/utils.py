from enum import Enum
from os.path import join, exists
from fastapi.exceptions import HTTPException


# ------------- for now --------------

base_path = '/mnt/e'

# ------------------------------------


class Directories(Enum):
    VIDEOS = 'videos'
    PHOTOS = 'photos'
    DOCUMENTS = 'documents'


def generate_file_path(file_slug: str, directory_name: Directories) -> str:
    return join(base_path, directory_name.value, file_slug)


def validate_file_existence(file_path: str) -> None:
    if not file_path:
        raise HTTPException(status_code=422, detail="Document slug cannot be empty")
    if not exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")

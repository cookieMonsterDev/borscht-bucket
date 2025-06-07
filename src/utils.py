from os.path import join
from mimetypes import guess_type
from settings import get_settings
from constants import Directories

settings = get_settings()


def generate_file_path(slug: str, directory: Directories) -> str:
    return join(settings.directory_path, directory.value, slug)


def generate_file_media_type(path: str) -> str:
    return guess_type(path)[0] or "text/plain"

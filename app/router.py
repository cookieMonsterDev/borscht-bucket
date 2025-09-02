from fastapi import APIRouter, Header, UploadFile
from services import files, videos, photos, documents

api_router = APIRouter()


@api_router.post("/upload")
async def upload_file(file: UploadFile):
    return await files.upload_file(file)


@api_router.get("/videos/{slug}")
async def get_video(slug: str, range_header: str = Header(None, alias="Range")):
    return await videos.get_video_by_slug(slug, range_header)


@api_router.get("/photos/{slug}")
async def get_photos(slug: str):
    return await photos.get_photo_by_slug(slug)


@api_router.get("/documents/{slug}")
async def get_document(slug: str):
    return await documents.get_document_by_slug(slug)


@api_router.delete("/{directory}/{slug}")
async def delete_file(directory: str, slug: str):
    return await files.delete_file(directory, slug)

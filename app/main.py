import exceptions
from typing import Annotated
from settings import get_settings
from fastapi.middleware.cors import CORSMiddleware
from services import files, videos, photos, documents
from fastapi import FastAPI, Header, UploadFile, BackgroundTasks

app = FastAPI()

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["GET", 'POST', 'OPTIONS'],
    allow_headers=["*"],
)

app.add_exception_handler(exceptions.HTTPException, exceptions.custom_http_exception_handler)
app.add_exception_handler(exceptions.StarletteHTTPException, exceptions.starlette_http_exception_handler)
app.add_exception_handler(exceptions.RequestValidationError, exceptions.validation_exception_handler)


@app.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    return await files.upload_file(file, background_tasks)


@app.get("/videos/{slug}")
async def get_video(slug: str, range: str = Header(None)):
    return await videos.get_video_by_slug(slug, range)


@app.get("/photos/{slug}")
async def get_doucment(slug: str):
    return await photos.get_photo_by_slug(slug)


@app.get("/documents/{slug}")
async def get_doucment(slug: str):
    return await documents.get_document_by_slug(slug)


@app.delete("/{directory}/{slug}")
async def delete_file(directory: str, slug: str):
    return await files.delete_file(directory, slug)

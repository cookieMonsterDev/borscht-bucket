from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from services import uploads, videos, photos, documents


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: UploadFile):
    return await uploads.upload_file(file)


@app.get("/videos/{slug}")
async def get_video(slug: str):
    return await videos.get_video_by_slug(slug)


@app.get("/photos/{slug}")
async def get_doucment(slug: str):
    return await photos.get_photo_by_slug(slug)


@app.get("/documents/{slug}")
async def get_doucment(slug: str):
    return await documents.get_document_by_slug(slug)

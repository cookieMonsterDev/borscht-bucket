from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from config import Settings, get_settings
from services import videos, photos, documents
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: bytes):
    return {"message": "File uploaded successfully."}


@app.get("/videos/{video_slug}")
async def get_video(video_slug: str, settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": f"This is a video endpoint for {video_slug}."}


@app.get("/photos/{photo_slug}")
async def get_doucment(photo_slug: str, settings: Annotated[Settings, Depends(get_settings)]):
    return photos.get_photo_by_slug(document_slug=photo_slug)


@app.get("/documents/{document_slug}")
async def get_doucment(document_slug: str, settings: Annotated[Settings, Depends(get_settings)]):
    return documents.get_document_by_slug(document_slug=document_slug)

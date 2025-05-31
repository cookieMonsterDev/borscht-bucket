from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from config import Settings, get_settings

app = FastAPI()


@app.get("/files")
async def upload_file(settings: Annotated[Settings, Depends(get_settings)]):
    return {"Hello": settings.directory_path}

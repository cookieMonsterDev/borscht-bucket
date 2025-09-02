import exceptions
from fastapi import FastAPI
from router import api_router
from settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.add_exception_handler(exceptions.HTTPException, exceptions.custom_http_exception_handler)
app.add_exception_handler(exceptions.StarletteHTTPException, exceptions.starlette_http_exception_handler)
app.add_exception_handler(exceptions.RequestValidationError, exceptions.validation_exception_handler)

app.include_router(api_router)

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class HTTPException(Exception):
    def __init__(self, status: int = 500, error: str = 'Internal Server Error', message: str = 'Something went wrong'):
        self.status = status
        self.error = error
        self.message = message


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status=400, error="Bad Request", message=message)


class NotFoundException(HTTPException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status=404, error="Not Found", message=message)


async def custom_http_exception_handler(_: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status,
        content={"status": exception.status, "error": exception.error, "message": exception.message},
    )


async def starlette_http_exception_handler(_: Request, exception: StarletteHTTPException):
    error = exception.detail if isinstance(exception.detail, str) else "HTTP Error"
    message = "The requested resource was not found" if exception.status_code == 404 else str(exception.detail)
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status": exception.status_code,
            "error": error,
            "message": message,
        },
    )


async def validation_exception_handler(_: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error": "Validation Error",
            "message": exception.errors(),
        },
    )

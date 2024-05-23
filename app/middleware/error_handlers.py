from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates/")

def add_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    @app.exception_handler(StarletteHTTPException)
    @app.exception_handler(ValidationError)
    @app.exception_handler(HTTPException)
    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception):
        status_code = 500
        message = ''

        if isinstance(exc, HTTPException):
            status_code = exc.status_code
            message = exc.detail
        elif isinstance(exc, RequestValidationError) or isinstance(exc, ValidationError):
            status_code = 400
            message = "Validation Error"
        elif isinstance(exc, StarletteHTTPException):
            status_code = exc.status_code
            message = exc.detail
        elif isinstance(exc, HTTPException):
            status_code = exc.status_code
            message = exc.detail
        else:
            message = "Internal Server Error"

        return templates.TemplateResponse("errors/errors.html", {"request": request, "message": message}, status_code=status_code)

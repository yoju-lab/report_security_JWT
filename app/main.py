from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os

from app.database.connection import Settings
from app.middleware.auth import auth_middleware
from app.routes import users, common_codes, comodules, mains, securities, errors, communities, boards

app = FastAPI()

settings = Settings()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.middleware("http")(auth_middleware)

# Routes
app.include_router(users.router, prefix="/users")
app.include_router(common_codes.router, prefix="/commoncodes")
app.include_router(comodules.router, prefix="/comodules")
app.include_router(comodules.router, prefix="/devtemplates")
app.include_router(comodules.router, prefix="/teams")
app.include_router(mains.router, prefix="/mains")
app.include_router(securities.router, prefix="/securities")
app.include_router(errors.router, prefix="/errors")
app.include_router(communities.router, prefix="/communities")
app.include_router(boards.router, prefix="/boards")

# Static Files
app.mount("/css", StaticFiles(directory=os.path.join("app", "resources", "css")), name="static_css")
app.mount("/images", StaticFiles(directory=os.path.join("app", "resources", "images")), name="static_images")
app.mount("/js", StaticFiles(directory=os.path.join("app", "resources", "js")), name="static_js")
app.mount("/downloads", StaticFiles(directory=os.path.join("app", "resources", "downloads")), name="static_downloads")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates/")

@app.get("/")
async def root():
    return RedirectResponse(url="/mains/list")

from app.middleware.auth import log_request_response
from fastapi import Request, Response
import time

@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    response = await call_next(request)
    await log_request_response(request, response, request.state.user)
    return response

# Error Handler
from app.middleware.error_handlers import add_error_handlers

add_error_handlers(app)

if __name__ == '__main__':
    pass
    # uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

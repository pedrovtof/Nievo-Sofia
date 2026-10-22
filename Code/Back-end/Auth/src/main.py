"""Setup FastAPI application with environment variables and CORS middleware."""
from http import HTTPStatus
import os

from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from api.router import api_router
from core.logging import CustomLogger
from core.middleware.server_exception_handler import ServerExceptionHandler

load_dotenv()

log = CustomLogger(__name__)

app = FastAPI(
    telemetry={"tracing": os.getenv("TELEMETRY_TRACING", False)},
    debug=os.getenv("DEBUG", False),
    title=os.getenv("APP_NAME", "FastAPI Application"),
    description=os.getenv("APP_DESCRIPTION", "This is a FastAPI application."),
    version=os.getenv("APP_VERSION", "1.0.0"),
    contact={
        "name": os.getenv("CONTACT_NAME", "API Support"),
        "url": os.getenv("CONTACT_URL", "http://www.example.com/support"),
        "email": os.getenv("CONTACT_EMAIL", "support@example.com")
    },
    license_info={
        "name": os.getenv("LICENSE_NAME", "Apache 2.0"),
        "url": os.getenv("LICENSE_URL", "http://www.apache.org/licenses/LICENSE-2.0.html")
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPStatus.INTERNAL_SERVER_ERROR)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions in the FastAPI application."""
    handler = ServerExceptionHandler(request, exc)
    return await handler.handle_exception()

log.info(f"FastAPI application '{os.getenv('APP_NAME', 'FastAPI Application')}' is running in {os.getenv('ENVIRONMENT', 'development')} mode version {os.getenv('APP_VERSION', '1.0.0')}.")

app.include_router(api_router, prefix="/api")

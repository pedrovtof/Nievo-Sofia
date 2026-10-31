"""Setup FastAPI application with environment variables, database lifespan, and CORS middleware."""
from contextlib import asynccontextmanager
from http import HTTPStatus
import os

from api.router import api_router
from core.database.session_manager import SessionManager
from core.logging import CustomLogger
from core.middleware.server_exception_handler import ServerExceptionHandler
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

log = CustomLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manage startup and shutdown lifecycle events for the Auth database connection pool."""
    db_url = os.getenv("PGSQL_DATABASE_PLATFORM_AUTH_ACCOUNTS_CONNECTION_STRING")
    if db_url:
        SessionManager.initialize(db_url=db_url)
        log.info("Database SessionManager initialized successfully.")
    else:
        log.warning(
            "PGSQL_DATABASE_PLATFORM_AUTH_ACCOUNTS_CONNECTION_STRING is not configured; "
            "SessionManager initialization skipped at startup."
        )
    try:
        yield
    finally:
        SessionManager.close()

app = FastAPI(
    lifespan=lifespan,
    telemetry={"tracing": os.getenv("TELEMETRY_TRACING", "False").lower() == "true"},
    debug=os.getenv("DEBUG", "False").lower() == "true",
    title=os.getenv("APP_NAME", "FastAPI Application"),
    description=os.getenv("APP_DESCRIPTION", "This is a FastAPI application."),
    version=os.getenv("APP_VERSION", "1.0.0"),
    contact={
        "name": os.getenv("CONTACT_NAME", "API Support"),
        "url": os.getenv("CONTACT_URL", "http://www.example.com/support"),
        "email": os.getenv("CONTACT_EMAIL", "support@example.com"),
    },
    license_info={
        "name": os.getenv("LICENSE_NAME", "Apache 2.0"),
        "url": os.getenv("LICENSE_URL", "http://www.apache.org/licenses/LICENSE-2.0.html"),
    },
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


log.info(
    f"FastAPI application '{os.getenv('APP_NAME', 'FastAPI Application')}' is running "
    f"in {os.getenv('ENVIRONMENT', 'development')} mode version {os.getenv('APP_VERSION', '1.0.0')}."
)

app.include_router(api_router, prefix="/api")

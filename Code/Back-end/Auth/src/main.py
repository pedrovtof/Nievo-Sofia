"""Setup FastAPI application with environment variables and CORS middleware."""

import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

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

print(f"\n\nFastAPI application '{os.getenv('APP_NAME', 'FastAPI Application')}' is running in {os.getenv('ENVIRONMENT', 'development')} mode version {os.getenv('APP_VERSION', '1.0.0')}.\n\n")

@app.get("/health")
async def read_root():
    return {"message": "alive"}


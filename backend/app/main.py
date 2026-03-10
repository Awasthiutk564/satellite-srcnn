from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes import auth, enhance, images
from app.core.config import settings
from app.utils.file_storage import STORAGE_ROOT, _ensure_directories


def create_app() -> FastAPI:
    app = FastAPI(
        title="SatEnhance AI Backend",
        version="0.1.0",
        description="FastAPI backend for SatEnhance AI – Satellite Image Super-Resolution Platform",
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Ensure storage directories exist before mounting
    _ensure_directories()

    # Static files for stored images
    app.mount(
        "/files",
        StaticFiles(directory=str(STORAGE_ROOT)),
        name="files",
    )

    # API routes
    api_prefix = settings.API_V1_STR
    app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["auth"])
    app.include_router(images.router, prefix=f"{api_prefix}/images", tags=["images"])
    app.include_router(enhance.router, prefix=f"{api_prefix}/enhance", tags=["enhance"])

    # Simple health check
    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "app": "sat-enhance-ai-backend"}

    return app


app = create_app()

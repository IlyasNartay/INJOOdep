import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.api import register_routers
from app.config import (
    APP_TITLE,
    APP_VERSION,
    CORS_ALLOW_ORIGINS,
    UPLOAD_FOLDER,
)


def configure_openapi(app: FastAPI) -> None:
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=APP_VERSION,
            description="Restaurant API с JWT авторизацией",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        for path in openapi_schema["paths"].values():
            for operation in path.values():
                operation.setdefault("security", []).append({"BearerAuth": []})

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


def configure_static_files(app: FastAPI) -> None:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.mount(
        "/uploaded_images",
        StaticFiles(directory=UPLOAD_FOLDER),
        name="uploaded_images",
    )


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(title=APP_TITLE, version=APP_VERSION)
    configure_openapi(app)
    configure_static_files(app)
    configure_middleware(app)
    register_routers(app)
    return app

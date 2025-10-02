from fastapi import FastAPI
from app.routers import auth, menu, order, address
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app import models
from telegram_bot.bot_instance import bot, dp
from fastapi.staticfiles import StaticFiles
import asyncio
from fastapi.openapi.utils import get_openapi
import os

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Restaurant API")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Restaurant API с JWT авторизацией",
        routes=app.routes,
    )

    # Добавляем схему авторизации (Bearer token)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Применяем ко всем ручкам
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_FOLDER), name="uploaded_images")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(menu.router, prefix="/api/menu", tags=["Menu"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(address.router, prefix="/addresses", tags=["Addresses"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],   # Разрешить все HTTP методы (GET, POST и т.д.)
    allow_headers=["*"],   # Разрешить все заголовки (включая Authorization и Content-Type)
)

@app.on_event("startup")
async def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
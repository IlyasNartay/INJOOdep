import os


APP_TITLE = os.getenv("APP_TITLE", "Restaurant API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploaded_images")

_raw_cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
CORS_ALLOW_ORIGINS = [
    origin.strip()
    for origin in _raw_cors_origins.split(",")
    if origin.strip()
] or ["*"]

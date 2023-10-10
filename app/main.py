# app/main.py
from fastapi import FastAPI

# Импортируем главный роутер.
from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title)

# Подключаем главный роутер.
app.include_router(main_router)

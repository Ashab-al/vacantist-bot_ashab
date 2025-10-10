"""
Модуль объединяет маршруты (роутеры) для работы с категориями в FastAPI.

Импорты:
- create_router: роутер для создания новых категорий.
- destroy_router: роутер для удаления категорий.
- list_router: роутер для получения списка категорий.
- show_router: роутер для получения информации о конкретной категории.
- update_router: роутер для обновления информации о категории.
- APIRouter: класс FastAPI для объединения маршрутов в один роутер.

Назначение модуля:
- Создаёт единый `categories_router`, который агрегирует все роутеры категорий.
- Используется для подключения к основному приложению FastAPI 
через `app.include_router(categories_router)`.
"""
from api.categories.create import router as create_router
from api.categories.destroy import router as destroy_router
from api.categories.list import router as list_router
from api.categories.show import router as show_router
from api.categories.update import router as update_router
from fastapi import APIRouter

categories_router = APIRouter()

categories_router.include_router(create_router)
categories_router.include_router(destroy_router)
categories_router.include_router(list_router)
categories_router.include_router(show_router)
categories_router.include_router(update_router)

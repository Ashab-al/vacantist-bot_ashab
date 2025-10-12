"""
Модуль объединяет маршруты (роутеры) для работы с вакансиями в FastAPI.

Импорты:
- create_router: роутер для создания новых вакансий.
- list_router: роутер для получения списка вакансий.
- APIRouter: класс FastAPI для объединения маршрутов в один роутер.

Назначение модуля:
- Создаёт единый `vacancies_router`, который агрегирует все роутеры вакансий.
- Используется для подключения к основному приложению FastAPI
через `app.include_router(vacancies_router)`.
"""

from api.vacancies.create import router as create_router
from api.vacancies.list import router as list_router
from fastapi import APIRouter

vacancies_router = APIRouter()

vacancies_router.include_router(create_router)
vacancies_router.include_router(list_router)

"""
Модуль объединяет все основные роутеры API в один общий роутер для FastAPI.

Импорты:
- categories_router: роутер для работы с категориями.
- users_router: роутер для работы с пользователями.
- vacancies_router: роутер для работы с вакансиями.
- APIRouter: класс FastAPI для объединения маршрутов в один роутер.

Назначение модуля:
- Создаёт единый `api_router`, который агрегирует все роутеры проекта.
- Устанавливает префиксы и теги для каждого роутера.
- Используется для подключения к основному приложению FastAPI
через `app.include_router(api_router)`.
"""

from api.categories import categories_router
from api.users import users_router
from api.vacancies import vacancies_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(vacancies_router, prefix="/vacancies", tags=["Vacancy"])
api_router.include_router(categories_router, prefix="/categories", tags=["Category"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])

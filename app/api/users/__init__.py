"""
Модуль объединяет маршруты (роутеры) для работы с пользователями в FastAPI.

Импорты:
- list_router: роутер для получения списка пользователей.
- mail_all_router: роутер для рассылки сообщений всем пользователям.
- set_bonus_router: роутер для назначения бонусов пользователям.
- set_status_router: роутер для изменения статуса пользователей.
- show_router: роутер для получения информации о конкретном пользователе.
- APIRouter: класс FastAPI для объединения маршрутов в один роутер.

Назначение модуля:
- Создаёт единый `users_router`, который агрегирует все роутеры пользователей.
- Используется для подключения к основному приложению FastAPI 
через `app.include_router(users_router)`.
"""
from api.users.list import router as list_router
from api.users.mail_all import router as mail_all_router
from api.users.set_bonus import router as set_bonus_router
from api.users.set_status import router as set_status_router
from api.users.show import router as show_router
from fastapi import APIRouter

users_router = APIRouter()

users_router.include_router(list_router)
users_router.include_router(show_router)
users_router.include_router(set_status_router)
users_router.include_router(set_bonus_router)
users_router.include_router(mail_all_router)

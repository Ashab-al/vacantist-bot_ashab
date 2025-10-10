from fastapi import APIRouter

from api.vacancies.create import router as create_router
from api.vacancies.list import router as list_router

vacancies_router = APIRouter()

vacancies_router.include_router(create_router)
vacancies_router.include_router(list_router)

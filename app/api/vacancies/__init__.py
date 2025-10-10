from api.vacancies.create import router as create_router
from api.vacancies.list import router as list_router
from fastapi import APIRouter

vacancies_router = APIRouter()

vacancies_router.include_router(create_router)
vacancies_router.include_router(list_router)

from fastapi import APIRouter

from api.vacancies.create import router as create_router

vacancies_router = APIRouter()

vacancies_router.include_router(create_router)
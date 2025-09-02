from fastapi import APIRouter
from api.vacancies import vacancies_router

api_router = APIRouter()

api_router.include_router(vacancies_router, prefix="/vacancies", tags=["Vacancy"])
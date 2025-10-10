from api.categories import categories_router
from api.users import users_router
from api.vacancies import vacancies_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(vacancies_router, prefix="/vacancies", tags=["Vacancy"])
api_router.include_router(categories_router, prefix="/categories", tags=["Category"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])

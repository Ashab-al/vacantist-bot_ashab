from fastapi import APIRouter
from api.users.list import router as list_router

users_router = APIRouter()

users_router.include_router(list_router)
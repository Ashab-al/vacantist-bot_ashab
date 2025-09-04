from fastapi import APIRouter
from api.users.list import router as list_router
from api.users.show import router as show_router


users_router = APIRouter()

users_router.include_router(list_router)
users_router.include_router(show_router)
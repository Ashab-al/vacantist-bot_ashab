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

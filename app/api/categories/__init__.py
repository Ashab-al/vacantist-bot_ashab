from api.categories.create import router as create_router
from api.categories.destroy import router as destroy_router
from api.categories.list import router as list_router
from api.categories.show import router as show_router
from api.categories.update import router as update_router
from fastapi import APIRouter

categories_router = APIRouter()

categories_router.include_router(create_router)
categories_router.include_router(destroy_router)
categories_router.include_router(list_router)
categories_router.include_router(show_router)
categories_router.include_router(update_router)

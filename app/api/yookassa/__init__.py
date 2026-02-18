from api.yookassa.success import router as success_router
from fastapi import APIRouter

yookassa_router = APIRouter()

yookassa_router.include_router(success_router)

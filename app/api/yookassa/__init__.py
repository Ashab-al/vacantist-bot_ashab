from fastapi import APIRouter

from api.yookassa.success import router as success_router


yookassa_router = APIRouter()

yookassa_router.include_router(success_router)

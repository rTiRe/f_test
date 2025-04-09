from fastapi import APIRouter

from src.api.v1.tron.router import router as tron_router


router = APIRouter(prefix='/v1')
router.include_router(tron_router)

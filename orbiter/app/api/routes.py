# app/api/routes.py
from fastapi import APIRouter
from app.api.block import block_router
from app.api.sidechain_router import sc_router 
from app.api.database_router import db_router

router = APIRouter()

router.include_router(block_router)
router.include_router(sc_router)
router.include_router(db_router)

@router.get("/status")
async def status():
    return {"status": "Orbiter is up"}

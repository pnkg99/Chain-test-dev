# app/api/sidechain.py

from fastapi import APIRouter, HTTPException
from app.models.sidechain import SidechainRegisterRequest
from app.services.sidechain_service import register_sidechain, get_registerd_sidechains, get_registerd_sidechain, get_sidechain_status
from app.services.chain_services import get_info

sc_router = APIRouter(prefix="/sidechain", tags=["Sidechain"])

@sc_router.post("/register")
async def register_new_sidechain(request: SidechainRegisterRequest):
    result = register_sidechain(request)
    if result["status"] == "fail":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@sc_router.get("/get")
async def get_sidechains(chain_name : str = ""):
    if chain_name :
        result = get_registerd_sidechain(chain_name)
    else :
        result = get_registerd_sidechains()
    return result

@sc_router.get("/status/{chain_name}")
async def get_sidechains(chain_name : str):
    result = get_sidechain_status(chain_name)
    if result["status"] == "fail":
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]
# app/api/sidechain.py

from fastapi import APIRouter, HTTPException
from app.models.database import DatabaseCreateRequest, SetDatabaseStructure
from app.services.database import create_database_service, set_database_structure, get_database_info

db_router = APIRouter(prefix="/database", tags=["Sidechain"])

@db_router.get("/get")
async def get_database(database_name : str ):
    result = get_database_info(database_name)
    if result["status"] == "fail":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@db_router.post("/create")
async def create_database(request: DatabaseCreateRequest):
    result = create_database_service(request)
    if result["status"] == "fail":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@db_router.post("/set_contract")
async def set_contract(request: SetDatabaseStructure):
    result = set_database_structure(request)
    if result["status"] == "fail":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

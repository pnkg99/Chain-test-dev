from fastapi import APIRouter
from app.services.chain_services import get_block_with_meta, get_block_transactions, get_block_actions

block_router = APIRouter(prefix="/block", tags=["Block"])

@block_router.get("/{block_number}")
async def get_block(block_number: int):
    block = get_block_with_meta(block_number)
    return {"data": block}

@block_router.get("/{block_number}/transactions")
async def get_block_tx(block_number: int, limit: int = 10, offset: int = 0):
    tx = get_block_transactions(block_number, limit, offset)
    return {"data": tx}

@block_router.get("/{block_number}/actions")
async def get_block_tx(block_number: int, limit: int = 10, offset: int = 0):
    tx = get_block_actions(block_number, limit, offset)
    return {"data": tx}

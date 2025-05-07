# app/services/block_service.py
from app.core.utils import safe_chain_call
from app.core.config import settings

def get_info(url) :
    try :
        info = safe_chain_call(url, "get_info")
        return info
    except :
        return None

def get_block(block_number):
    block = safe_chain_call(settings.MASTER_CHAIN_URL, "get_block", block_number)
    return block

def get_block_with_meta(block_number: int) :
    block = get_block(block_number)
    block["transactions"] = len(block.get("transactions", []))
    return block

def get_block_transactions(block_number: int, limit: int = 10, offset: int = 0):
    block = get_block(block_number)
    transactions = block.get("transactions", [])[offset:offset + limit]
    return  transactions

def get_block_actions(block_number: int, limit: int = 50, offset: int = 0) :
    transactions = get_block_transactions(block_number, limit=1000000)
    actions = []
    for transaction in transactions :
        for action in transaction["trx"]["transaction"]["actions"] :
            actions.append(action)
    return actions[offset:offset+limit]
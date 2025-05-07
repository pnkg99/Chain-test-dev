from app.models.sidechain import SidechainRegisterRequest
from app.core.utils import safe_chain_call, hash_name, execute_orbiter_action
from app.core.config import settings
from app.services.chain_services import get_info
from collections import defaultdict

def get_sidechain_url(chain_name : str):
    sidechain = get_registerd_sidechain(chain_name)
    if sidechain:
        try :
            url = sidechain["rpc_url"][0]
            return {"status" : "success", "data":url}
        except : 
            return {"status" : "fail", "message" : "Sidechain don't have any url"}
    else : 
        return {"status" : "fail", "message" : "Sidechain don't exists"}

def get_sidechain_status(chain_name : str):
    response = get_sidechain_url(chain_name)
    if response["status"] == "fail":
        return response
    else :
        sidechain_info = get_info(response["data"])
        if sidechain_info :
            return {"status" : "success", "data": sidechain_info}
        else :
            return {"status" : "fail", "message":"Sidechain is not currently available"}


def get_registerd_sidechains(): 
    side_chains = safe_chain_call(settings.MASTER_CHAIN_URL, "get_table", settings.ORBITER_ACCOUNT, settings.ORBITER_ACCOUNT, "sidechains", )["rows"]
    side_chains_urls = safe_chain_call(settings.MASTER_CHAIN_URL, "get_table", settings.ORBITER_ACCOUNT, settings.ORBITER_ACCOUNT, "nodeurls", )["rows"]
    # Spojimo dve liste recnika 
    urls_map = defaultdict(list)
    for url in side_chains_urls :
        urls_map[url["chain_name"]].append(url["rpc_url"])
    result = [{**entry, "rpc_url": urls_map.get(entry["chain_name"], [])} for entry in side_chains]
    return result

def get_registerd_sidechain(chain_name):
    
    hash = hash_name(chain_name)    
    side_chain = safe_chain_call(settings.MASTER_CHAIN_URL, "get_table", settings.ORBITER_ACCOUNT, settings.ORBITER_ACCOUNT, "sidechains", "1", "i64", hash,hash,"1")["rows"]
    if len(side_chain) != 1 :
        return {}
    side_chain_urls = safe_chain_call(settings.MASTER_CHAIN_URL, "get_table", settings.ORBITER_ACCOUNT, settings.ORBITER_ACCOUNT, "nodeurls", "2", "i64", hash,hash,"20" )["rows"]
    urls_map = defaultdict(list)
    for url in side_chain_urls :
        urls_map[url["chain_name"]].append(url["rpc_url"])
    result = [{**entry, "rpc_url": urls_map.get(entry["chain_name"], [])} for entry in side_chain]
    return result[0]
    
def register_sidechain(data: SidechainRegisterRequest):

    # Validacija sidechain-a
    if str(data.rpc_url) == settings.MASTER_CHAIN_URL :
        return {"status": "fail", "message": "Sidechain url can't be same as Masterchain url"}
    
    info = get_info(data.rpc_url)
    if not info : return {"status": "fail", "message": "Sidechain rpc_url is not valid"}

    sidechain_registry = get_registerd_sidechains()
    
    for chain in sidechain_registry:
        if chain['chain_name'] == data.name or data.rpc_url in chain['rpc_url']:
            return {"status": "fail", "message": "Sidechain already registered."}
    
    # Transakcija ka master chain-u
    
    sidechain_entry = {
        "chain_name": data.name,
        "rpc_url": str(data.rpc_url),
        "description": data.description
    }
    
    execute_orbiter_action("regsidechain", sidechain_entry)

    return {"status": "success", "message": "Sidechain registered successfully.", "data": sidechain_entry}

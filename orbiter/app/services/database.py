from app.models.database import DatabaseCreateRequest, SetDatabaseStructure
from app.core.utils import safe_chain_call, execute_orbiter_action
from app.core.config import settings
from app.services.sidechain_service import get_sidechain_url
from binascii import hexlify
import json

master_chain = settings.MASTER_CHAIN_NAME
master_url = settings.MASTER_CHAIN_URL

def database_exists(chain_url : str, database_name : str) :
    try:
        safe_chain_call(chain_url, "get_account", database_name)
        return True
    except:
        return False

def get_database_from_blockchain(chain_url : str, database_name : str) :
    try:
        out = safe_chain_call(chain_url, "get_account", database_name)
        return out
    except:
        return None

def get_value_contract_from_blockchain(chain_url: str, database_name : str):
    try :
        contract = safe_chain_call(chain_url, "get_code", database_name)
        return contract
    except Exception as e :
        print(e)
        return None

def get_database_owner_public_key(chain_url : str, database_name : str) :
    try : 
        account = safe_chain_call(chain_url, "get_account", database_name)
        account_pkey = account["permissions"][0]["required_auth"]["keys"][0]["key"]
        return account_pkey
    except : return None

def get_database_info(database_name, sidechain_url=""):
    db = get_database_from_blockchain(master_url, database_name)
    if not db:
        return {"status": "fail", "message": f"Database '{database_name}' don't exists on master chain `{master_chain}`."}
    vc = get_value_contract_from_blockchain(master_url, database_name)

    return {"status": "success", "info" : db, "value_contract" : vc}

def create_database_service(data: DatabaseCreateRequest):
    database_name = data.database_name
    sidechain = data.sidechain_name

    # Samo za master_chain
    if sidechain == master_chain:
        if database_exists(master_url, database_name) : 
            return {"status": "fail", "message": f"Database '{database_name}' already exists on master chain `{master_chain}`."}
        else:
            safe_chain_call(master_url, "create_account", database_name, data.database_pubkey)
            return {"status": "success", "message": f"Database '{database_name}' created on master chain `{master_chain}`."}

    # Flow za sidechain 
    else: 
        url_response = get_sidechain_url(sidechain)
        if url_response["status"] == "fail":
            return url_response
        else :
            sidechain_url = url_response["data"]
            # Proveri da li postoji baza vec na master chainu
            account_pkey = get_database_owner_public_key(master_url, database_name)
            if not account_pkey :
                account_pkey = data.database_pubkey
                safe_chain_call(master_url, "create_account", database_name, account_pkey)
                safe_chain_call(sidechain_url, "create_account", database_name, account_pkey)
                message = f"Database '{database_name}' created on both {master_chain} and {sidechain}."
            else :
                safe_chain_call(sidechain_url, "create_account", database_name, account_pkey)
                message = f"Database '{database_name}' already existed on master chain {master_chain}  and created on {sidechain} with public key from master chain: {account_pkey}"
            
            execute_orbiter_action("adddatabase", {"db_name": database_name, "chain_name": sidechain})
            
            return {
                "status": "success",
                "message": message
            }

def set_database_structure(data : SetDatabaseStructure):
    sidechain_name = data.sidechain_name
    database_name = data.database_name
    database_privatekey = data.database_privkey
    wasm = data.database_wasm
    abi = data.database_abi
    
    master_only = False
    
    if sidechain_name == master_chain:
        master_only = True
    else : 
        url_response = get_sidechain_url(sidechain_name)
        if url_response["status"] == "fail":
            return url_response
        else :
            url = url_response["data"]
    
    # Proveravamo postojanje baza
    if not database_exists(master_url, database_name) :
        return {"status" : "fail", "message" : f"Database {database_name} don't exists on master chain `{master_chain}`"}
    if not master_only and not database_exists(url, database_name):
        return {"status" : "fail", "message" : f"Database `{database_name}` don't exists on sidechain `{sidechain_name}`"}
    
    # proveravamo postojanje kontrakta
    master_vc = get_value_contract_from_blockchain(master_url, database_name)
    wasm = hexlify(bytes(master_vc["wasm"].encode()))
    # if abi in master_vc.keys() and master_vc["wasm"] :
    #     pass
    # wasm = master_vc["wasm"]
    # abi = master_vc["abi"]
    # print(bytes(wasm))
    # if not master_only :
    #     side_vc = get_value_contract_from_blockchain(url, database_name)
    #     # ako ne postoji konktrakt na sidechain-u 
    #     if "abi" not in side_vc.keys() and not side_vc["wasm"] :
    #         wasm = "asd"
            
            
    # Proveravamo validnost WASM-a i ABI-ja
    if not wasm : 
        with open("/home/petar/multi_chain/orbiter/contract/contract_1/database.wasm", 'rb') as rf:
            wasm = rf.read()
            hex_wasm = hexlify(wasm)
    else : hex_wasm = wasm
    if not abi :
        with open("/home/petar/multi_chain/orbiter/contract/contract_1/database.abi", 'rb') as rf:
            abi_json = json.load(rf)
    else : abi_json = abi
   
   # Setujemo Konktrakt na Master i na sidechain ako treba
    try :
        safe_chain_call(master_url, "set_code", database_name, hex_wasm, database_privatekey, "code_raw=True")
        safe_chain_call(master_url, "set_abi", database_name, abi_json, database_privatekey, "abi_json=True")
        message = f"Value Contract set on database `{database_name}` on `{settings.MASTER_CHAIN_NAME}`"
        if not master_only :
            safe_chain_call(url, "set_code", database_name, hex_wasm, database_privatekey, "code_raw=True")
            safe_chain_call(url, "set_abi", database_name, abi_json, database_privatekey, "abi_json=True")
            message = f"Value Contract set on database `{database_name}` on master chain `{settings.MASTER_CHAIN_NAME}` and sidechain `{sidechain_name}`"
        return {"status": "successful", "message" : message}
    except Exception as e :
        return {"status": "fail", "message" : str(e)}
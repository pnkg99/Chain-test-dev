# app/core/utils.py

from fastapi import HTTPException
import json
from app.services.inery.cline import Cline
from requests.exceptions import ConnectionError, Timeout
from app.core.config import settings
from app.services.inery.keys import INRKey

KEY = INRKey(settings.ORBITER_PK)

def execute_orbiter_action(action, entry_data):
    payload={
        "account": settings.ORBITER_ACCOUNT,
        "name": action,
        "authorization": [{
            "actor": settings.ORBITER_ACCOUNT,
            "permission": "active"
        }]
    }
    data = safe_chain_call(settings.MASTER_CHAIN_URL, "abi_json_to_bin", payload['account'], payload['name'], entry_data)
    payload['data'] = data['binargs']
    transaction =  {"actions": [payload]}
    out = safe_chain_call(settings.MASTER_CHAIN_URL, "push_transaction", transaction, KEY, "broadcast=True")
    return out

def safe_chain_call(url: str, method_name: str, *args, **kwargs):
    try:
        # Kreiraj CLI instancu sa URL-om
        cli = Cline(url=url)

        # Pozovi dinamičku metodu
        func = getattr(cli, method_name)
        return func(*args, **kwargs)
    
    except AttributeError:
        raise HTTPException(
            status_code=500,
            detail={"error": f"Method '{method_name}' not found in CLI client."}
        )
    except (ConnectionError, Timeout) as conn_err:
        # Specifična greška za problem sa konekcijom (URL ne postoji, server down)
        raise HTTPException(
            status_code=503,
            detail={"error": "Service unavailable", "raw": str(conn_err), "hint": "Check if Blockchain Node RPC endpoint is online and accessible."}
        )
    except Exception as e:
        # Pokušaj parsiranja greške
        try:
            parsed_error = json.loads(str(e)[7:].replace("'", "\""))
            status_code = parsed_error.get("code", 500)
            try : 
                parsed_error = parsed_error["error"]["details"][0]["message"]
            except :
                pass
        except Exception:
            status_code = 500
            parsed_error = {"error": "Unknown error", "raw": str(e)}

        raise HTTPException(status_code=status_code, detail=parsed_error)

def hash_name(name: str) :
    out = execute_orbiter_action("hsh", {"name" : name})
    return (out["processed"]['action_traces'][0]['console'])
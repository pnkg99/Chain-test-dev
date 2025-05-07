from pydantic import BaseModel, Field
from app.core.config import settings

class DatabaseCreateRequest(BaseModel):
    sidechain_name : str = Field(settings.MASTER_CHAIN_NAME, example="sidechain1")
    database_name: str = Field(..., example="dbname")
    database_pubkey: str = Field(..., example="INE8ddS6XQZ2NXEPbcLotWLtwKA3oNj7irQKqDebJNqJCnuPYfLu9")
    
class SetDatabaseStructure(BaseModel):
    sidechain_name : str = Field(settings.MASTER_CHAIN_NAME, example="sidechain1")
    database_name: str = Field(..., example="dbname")
    database_privkey: str = Field(..., example="")
    database_wasm : str = Field(None, example="")
    database_abi : str = Field(None, example="")
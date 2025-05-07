# app/models/sidechain.py

from pydantic import BaseModel, HttpUrl, Field

class SidechainRegisterRequest(BaseModel):
    name: str = Field(..., example="MySidechain")
    rpc_url: HttpUrl = Field(..., example="http://127.0.0.1:8888")
    description: str = Field(None, example="Optional description of the sidechain")

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Orbiter"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    MASTER_CHAIN_NAME : str = "master_chain"
    MASTER_CHAIN_URL: str="http://127.0.0.1:8888/"
    
    ORBITER_ACCOUNT : str = "orbiter"
    ORBITER_PK : str = "5Kct1aRac854KH6XDhAiPyYzp5DMzBhzhj2nanedNHVN3PSn7NR"

    class Config:
        env_file = ".env"

settings = Settings()
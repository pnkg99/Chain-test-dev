from fastapi import FastAPI
from app.api.routes import router as api_router
from fastapi.responses import FileResponse

app = FastAPI(title="Orbiter - Multi-Chain Orchestrator")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/public/blockchain.ico")

app.include_router(api_router, prefix="/api")
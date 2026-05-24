from fastapi  import FastAPI
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.core.init_db import init_db
from app.database import AsyncSessionLocal

async def lifespan(app: FastAPI):
    # Start an async db session on boot
    async with AsyncSessionLocal() as db:
        try: 
            print("INFO: DB tables and RBAC defaults loading...")
            await init_db(db)
            print("INFO: DB load successful.")
        except Exception as e:
            print(f"ERROR:  DB error: {e}")
    
    yield
    # Handle shutdown logic if needed here

# Initialize FastApi
app = FastAPI(
    title="Enterprise RBAC System API",
    description="A headless, logic-heavy backend engine for managing role-based user access controls.",
    version="0.1.0",
    lifespan=lifespan,
)

# Register auth router
app.include_router(auth_router)

# Verify server health
@app.get("/health", tags=["System"])
async def health_check() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "message": "The RBAC System engine is fully operational"}
    )
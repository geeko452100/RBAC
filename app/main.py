from fastapi  import FastAPI
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router

# Initialize FastApi
app = FastAPI(
    title="Enterprise RBAC System API",
    description="A headless, logic-heavy backend engine for managing role-based user access controls.",
    version="0.1.0",
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
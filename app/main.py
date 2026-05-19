from fastapi  import FastAPI
from fastapi.responses import JSONResponse

# Initialize FastApi
app = FastAPI(
    title="Enterprise RBAC System API",
    description="A headless, logic-heavy backend engine for managing role-based user access controls.",
    version="0.1.0",
)

# Verify server health
@app.get("/health", tags=["System"])
async def health_check() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "message": "The RBAC System engine is fully operational"}
    )
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AgenticFlow-Core API",
    description="Multi-agent workflow orchestrator for business automation",
    version="0.1.0",
)

class HealthCheck(BaseModel):
    status: str = "ok"

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the API is running."""
    return HealthCheck(status="ok")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

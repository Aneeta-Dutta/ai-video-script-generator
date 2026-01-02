"""
Simple web server wrapper for Cloud Run deployment.

Provides HTTP endpoint to trigger E2E pipeline execution.
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Video Production API")


class PipelineRequest(BaseModel):
    topic: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Video Production", "version": "v2"}


@app.get("/health")
async def health():
    """Health check for Cloud Run."""
    return {"status": "ok", "ready": True}


@app.post("/generate")
async def generate_video(request: PipelineRequest):
    """
    Generate research report and production script for a topic.
    
    Args:
        request: Pipeline request with topic
        
    Returns:
        Status and output information
    """
    import sys
    sys.path.insert(0, '/app')
    
    try:
        # Import here to avoid circular dependencies
        from run_e2e_sequential import run_pipeline
        
        # Run the E2E pipeline
        await run_pipeline(request.topic)
        
        return {
            "status": "success",
            "topic": request.topic,
            "message": "Pipeline completed successfully"
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "topic": request.topic,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

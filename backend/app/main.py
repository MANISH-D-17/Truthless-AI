from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api import verify, auth, knowledge, analytics
from app.services.vector_store import vector_store

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Healthcare Hallucination Detection & Fact Verification Platform backend API."
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting up Healthcare Hallucination Detection Platform...")
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"MongoDB connection notice: {e}")
    try:
        vector_store.initialize()
    except Exception as e:
        print(f"Vector Store initialization notice: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(verify.router, prefix=settings.API_V1_STR)
app.include_router(knowledge.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs",
        "verification_endpoint": f"{settings.API_V1_STR}/verify"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

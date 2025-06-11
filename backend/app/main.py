from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1 import patients, medications, prescriptions, ai_analysis, vector_store
from app.services.vector_store_manager import vector_store_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Initialize vector stores
    print("Initializing vector stores on startup...")
    try:
        await vector_store_manager.initialize()
        print("Vector stores initialization completed")
    except Exception as e:
        print(f"Warning: Vector store initialization failed: {e}")
    
    yield
    
    # Shutdown: cleanup if needed
    print("Application shutdown")


# Create FastAPI app with lifespan manager
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(patients.router, prefix="/api/v1", tags=["patients"])
app.include_router(medications.router, prefix="/api/v1", tags=["medications"])
app.include_router(prescriptions.router, prefix="/api/v1", tags=["prescriptions"])
app.include_router(ai_analysis.router, prefix="/api/v1", tags=["ai-analysis"])
app.include_router(vector_store.router, prefix="/api/v1/vector-store", tags=["vector-store"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Enhanced health check with vector store status."""
    vector_stats = vector_store_manager.get_store_stats()
    
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.version,
        "vector_store": {
            "initialized": vector_stats["initialized"],
            "medication_count": vector_stats["medication_count"],
            "symptom_count": vector_stats["symptom_count"]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

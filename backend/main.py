from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .api.routes import disease_routes, soil_routes, yield_routes, market_routes, auth_routes
from .ml_models.disease_model import get_disease_classifier
from .ml_models.yield_model import get_yield_predictor
from .ml_models.soil_analyzer import get_soil_analyzer
from .services.database_service import supabase

app = FastAPI(
    title="SmartFarmingAI API",
    description="Dynamic AI-powered agriculture advisory system using Groq LLM and real-time data.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup. ML models will be lazy-loaded to save memory."""
    logger.info("Application starting (ML models will load on-demand)...")
    
    # Diagnostic logging for database connection
    from backend.config import settings
    logger.info(f"SUPABASE_URL set: {bool(settings.SUPABASE_URL)}")
    logger.info(f"SUPABASE_KEY set: {bool(settings.SUPABASE_KEY)}")
    logger.info(f"ENABLE_REAL_DB: {settings.ENABLE_REAL_DB}")
    
    if supabase:
        logger.info("✓ Database connection verified")
    else:
        logger.warning("✗ Database connection NOT initialized. Using mock mode.")
        if not settings.SUPABASE_URL:
            logger.warning("  → SUPABASE_URL is not set")
        if not settings.SUPABASE_KEY:
            logger.warning("  → SUPABASE_KEY is not set")
        if not settings.ENABLE_REAL_DB:
            logger.warning("  → ENABLE_REAL_DB is False (set to 'true' to enable)")
        
    logger.info("Application startup complete")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for production stability
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router, prefix="/api", tags=["Authentication"])
app.include_router(disease_routes.router, prefix="/api", tags=["Disease Detection"])
app.include_router(soil_routes.router, prefix="/api", tags=["Soil Health"])
app.include_router(yield_routes.router, prefix="/api", tags=["Yield Prediction"])
app.include_router(market_routes.router, prefix="/api", tags=["Market Insights"])

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc)},
    )

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {
        "message": "Welcome to SmartFarmingAI API",
        "status": "Running",
        "version": "1.0.0"
    }

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

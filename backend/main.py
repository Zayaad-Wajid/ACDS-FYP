"""
ACDS - Autonomous Cyber Defense System
========================================
Main FastAPI application with all API endpoints for threat detection,
response automation, feedback loops, and report generation.
"""

import os
import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import configuration
try:
    from config.settings import CORS_ORIGINS, API_PREFIX, API_VERSION
except ImportError:
    CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
    API_PREFIX = "/api/v1"
    API_VERSION = "v1"

# Import routers
try:
    from api.routes.threats import router as threats_router
    from api.routes.feedback import router as feedback_router
    from api.routes.reports import router as reports_router
    from api.routes.auth import router as auth_router
    from api.routes.dashboard import router as dashboard_router
    from api.routes.testing import router as testing_router
except ImportError as e:
    print(f"Warning: Could not import routers: {e}")
    threats_router = None
    feedback_router = None
    reports_router = None
    auth_router = None
    dashboard_router = None
    testing_router = None

# Import services for health check
try:
    from ml.phishing_service import get_phishing_service
    from agents.orchestrator_agent import get_orchestrator_agent
except ImportError:
    get_phishing_service = None
    get_orchestrator_agent = None


# Application startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print("=" * 50)
    print("ACDS Backend Starting...")
    print(f"API Version: {API_VERSION}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    
    # Initialize ML service
    if get_phishing_service:
        service = get_phishing_service()
        if service.is_model_loaded():
            print("✅ ML Model loaded successfully")
        else:
            print("⚠️ ML Model not loaded - running in fallback mode")
    
    # Initialize Orchestrator
    if get_orchestrator_agent:
        orchestrator = get_orchestrator_agent()
        stats = orchestrator.get_stats()
        agents_status = stats.get('agents_available', {})
        print(f"✅ Orchestrator initialized - Agents: {agents_status}")
    else:
        print("⚠️ Orchestrator not available")
    
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("ACDS Backend shutting down...")


# Create FastAPI application
app = FastAPI(
    title="ACDS - Autonomous Cyber Defense System",
    description="""
    AI-powered cybersecurity platform for phishing email detection,
    automated threat response, and security analytics.
    
    ## Features
    
    * **Threat Detection** - ML-based phishing email detection
    * **Automated Response** - Quarantine, block, and notify on threats
    * **Feedback Loop** - Continuous model improvement from user feedback
    * **AI Reports** - Automated security report generation
    * **Real-time Monitoring** - Dashboard and analytics
    
    ## Authentication
    
    Most endpoints require JWT authentication. Use `/api/v1/auth/login` to obtain a token.
    
    Default credentials (development only):
    - Email: admin@acds.com
    - Password: admin123
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
if threats_router:
    app.include_router(threats_router, prefix=API_PREFIX)
if feedback_router:
    app.include_router(feedback_router, prefix=API_PREFIX)
if reports_router:
    app.include_router(reports_router, prefix=API_PREFIX)
if auth_router:
    app.include_router(auth_router, prefix=API_PREFIX)
if dashboard_router:
    app.include_router(dashboard_router, prefix=API_PREFIX)
if testing_router:
    app.include_router(testing_router, prefix=API_PREFIX)


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "ACDS - Autonomous Cyber Defense System",
        "version": "1.0.0",
        "api_version": API_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "endpoints": {
            "auth": f"{API_PREFIX}/auth",
            "dashboard": f"{API_PREFIX}/dashboard",
            "threats": f"{API_PREFIX}/threats",
            "feedback": f"{API_PREFIX}/feedback",
            "reports": f"{API_PREFIX}/reports",
            "testing": f"{API_PREFIX}/testing",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "api": True,
            "ml_model": False,
            "orchestrator": False,
            "agents": {
                "detection": False,
                "explainability": False,
                "response": False
            }
        }
    }
    
    # Check ML service
    if get_phishing_service:
        try:
            service = get_phishing_service()
            health_status["services"]["ml_model"] = service.is_model_loaded()
        except:
            pass
    
    # Check Orchestrator and agents
    if get_orchestrator_agent:
        try:
            orchestrator = get_orchestrator_agent()
            stats = orchestrator.get_stats()
            health_status["services"]["orchestrator"] = True
            health_status["services"]["agents"] = stats.get('agents_available', {})
        except:
            pass
    
    # Overall status
    if not health_status["services"]["orchestrator"]:
        health_status["status"] = "degraded"
    
    return health_status


@app.get(f"{API_PREFIX}/status")
async def api_status():
    """Get detailed API status and statistics."""
    status = {
        "api_version": API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": "N/A",  # Would track actual uptime
        "endpoints_available": [],
        "statistics": {}
    }
    
    # List available endpoints
    if threats_router:
        status["endpoints_available"].append("threats")
    if feedback_router:
        status["endpoints_available"].append("feedback")
    if reports_router:
        status["endpoints_available"].append("reports")
    if auth_router:
        status["endpoints_available"].append("auth")
    
    # Get ML statistics
    if get_phishing_service:
        try:
            service = get_phishing_service()
            status["statistics"]["detection"] = service.get_stats()
        except:
            pass
    
    return status


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# =============================================================================
# QUICK TEST ENDPOINTS
# =============================================================================

@app.post(f"{API_PREFIX}/quick-scan")
async def quick_scan(content: str):
    """
    Quick endpoint to scan email content without full request body.
    For testing purposes.
    """
    if not get_phishing_service:
        raise HTTPException(status_code=503, detail="ML service not available")
    
    service = get_phishing_service()
    result = service.predict(content)
    
    return {
        "success": True,
        "is_phishing": result.get("is_phishing"),
        "confidence": result.get("confidence"),
        "severity": result.get("severity"),
        "recommendation": result.get("recommendation")
    }


# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


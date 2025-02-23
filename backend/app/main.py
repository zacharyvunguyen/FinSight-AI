from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import pdf, analysis
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Financial Document Analysis API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdf.router, prefix="/api/v1/pdf", tags=["PDF"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to FinSight AI API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
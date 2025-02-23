from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import pdf

app = FastAPI(
    title="FinSight AI API",
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

@app.get("/")
async def root():
    return {"message": "Welcome to FinSight AI API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
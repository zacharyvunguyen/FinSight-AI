import requests
import sys
import uvicorn
import fastapi
from pydantic_settings import BaseSettings

def verify_backend_setup():
    """Verify FastAPI backend setup and dependencies."""
    print("\n🔍 Verifying Backend Setup...")
    
    # Check package versions
    print(f"✅ FastAPI version: {fastapi.__version__}")
    print(f"✅ Uvicorn version: {uvicorn.__version__}")
    
    # Try to import our app
    try:
        from backend.app.main import app
        print("✅ Successfully imported FastAPI app")
    except Exception as e:
        print(f"❌ Failed to import FastAPI app: {str(e)}")
        return False
    
    # Try to import settings
    try:
        from backend.app.core.config import settings
        print("✅ Successfully loaded settings")
    except Exception as e:
        print(f"❌ Failed to load settings: {str(e)}")
        return False
    
    # Try to connect to the API (if it's running)
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API health check successful")
        else:
            print(f"❌ API returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("ℹ️ API server is not running (start with 'uvicorn backend.app.main:app --reload')")
    
    return True

if __name__ == "__main__":
    verify_backend_setup() 
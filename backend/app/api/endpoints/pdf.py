from fastapi import APIRouter, UploadFile, File, HTTPException
from ...core.config import settings
from ...services.storage import StorageService
from ...models.pdf import PDFResponse
from datetime import datetime

router = APIRouter()
storage_service = StorageService(settings.GCP_STORAGE_BUCKET)

@router.post("/upload/", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.
    
    - Validates file type
    - Computes file hash
    - Stores in Google Cloud Storage
    - Returns signed URL for access
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Upload file to GCS
        storage_path, file_hash = storage_service.upload_file(file.file, file.filename)
        
        # Generate signed URL
        signed_url = storage_service.generate_signed_url(storage_path)
        
        return PDFResponse(
            file_name=file.filename,
            file_hash=file_hash,
            upload_timestamp=datetime.now(),
            file_size=file.size,
            storage_path=storage_path,
            signed_url=signed_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
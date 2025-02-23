from fastapi import APIRouter, UploadFile, File, HTTPException
from ...core.config import settings
from ...services.storage import StorageService
from ...models.pdf import PDFResponse
from datetime import datetime
from ...services.firestore import FirestoreService
from ...services.extraction import ExtractionService
from ...services.bigquery import BigQueryService
from ...services.pinecone import PineconeService
import tempfile
import os
from fastapi.responses import JSONResponse

router = APIRouter()
storage_service = StorageService(settings.GCP_STORAGE_BUCKET)
firestore_service = FirestoreService()
extraction_service = ExtractionService()
bigquery_service = BigQueryService()
pinecone_service = PineconeService()

@router.post("/upload/", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.
    
    - Validates file type
    - Computes file hash
    - Stores in Google Cloud Storage
    - Returns signed URL for access
    """
    print(f"Received file: {file.filename}")
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        print("Computing hash...")
        file_hash = storage_service.compute_file_hash(file.file)
        print(f"Hash computed: {file_hash}")
        
        print("Checking duplicates...")
        # Check for duplicates
        if await firestore_service.check_duplicate(file_hash):
            return JSONResponse(
                status_code=409,
                content={"detail": "File already exists"}
            )
        
        # Save file temporarily for extraction
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.file.seek(0)
            tmp.write(file.file.read())
            tmp_path = tmp.name
        
        # Extract data
        extraction_result = await extraction_service.extract_data(
            tmp_path,
            file_hash
        )
        
        # Upload file to GCS
        file.file.seek(0)
        storage_path, _ = storage_service.upload_file(file.file, file.filename)
        signed_url = storage_service.generate_signed_url(storage_path)
        
        # Store metadata in Firestore
        metadata = {
            'file_name': file.filename,
            'file_size': file.size,
            'storage_path': storage_path,
            'content_type': file.content_type,
            'extracted_content': extraction_result['content'],
            'extraction_metadata': extraction_result['metadata']
        }
        await firestore_service.store_file_metadata(file_hash, metadata)
        
        # Store in BigQuery
        bigquery_service.store_pdf_data(
            file_hash=file_hash,
            file_name=file.filename,
            content=extraction_result['content'],
            extraction_status=extraction_result['metadata']['status'],
            job_id=extraction_result['metadata']['job_id']
        )
        
        # Store in Pinecone
        pinecone_service.store_embeddings(
            content=extraction_result['content'],
            metadata={
                'file_hash': file_hash,
                'file_name': file.filename,
                'storage_path': storage_path
            }
        )
        
        # Cleanup temp file
        os.unlink(tmp_path)
        
        return PDFResponse(
            file_name=file.filename,
            file_hash=file_hash,
            upload_timestamp=datetime.now(),
            file_size=file.size,
            storage_path=storage_path,
            signed_url=signed_url,
            extraction_status=extraction_result['metadata']['status']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
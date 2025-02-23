# FinSight AI Backend

## Features
- PDF Upload API with deduplication
- Google Cloud Storage integration
- Secure file access with signed URLs
- Firestore metadata storage
- Duplicate file detection
- SHA-256 hash verification

## Structure
```
backend/
├── app/
│   ├── api/        # API endpoints
│   │   └── endpoints/
│   │       └── pdf.py    # PDF upload endpoint with deduplication
│   ├── core/       # Core configurations
│   ├── models/     # Data models
│   ├── services/   # Business logic
│   │   ├── storage.py    # GCS storage service
│   │   └── firestore.py  # Firestore metadata service
│   └── utils/      # Utility functions
└── tests/          # Backend tests
```

## Configuration
The backend uses pydantic-settings for configuration management. All settings are loaded from environment variables defined in `.env`.

### Required Environment Variables:
- **API Settings**
  - `API_V1_STR`: API version string
  - `PROJECT_NAME`: Project name

- **Google Cloud**
  - `GOOGLE_CLOUD_PROJECT`: GCP project ID
  - `GCP_STORAGE_BUCKET`: Storage bucket name
  - `BIGQUERY_DATASET`: BigQuery dataset name
  - `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key

- **Pinecone**
  - `PINECONE_API_KEY`: Pinecone API key
  - `PINECONE_CLOUD`: Cloud provider (aws)
  - `PINECONE_REGION`: Region (e.g., us-east-1)
  - `PINECONE_INDEX_NAME`: Index name
  - `PINECONE_ENVIRONMENT`: Pinecone environment

- **OpenAI**
  - `OPENAI_API_KEY`: OpenAI API key

## Development
1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run the development server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

3. Verify setup:
   ```bash
   python scripts/verify_backend.py
   ```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### PDF Upload
- **Endpoint**: `/api/v1/pdf/upload/`
- **Method**: POST
- **Description**: Upload PDF files to Google Cloud Storage
- **Features**:
  - File type validation
  - SHA-256 hash generation
  - Organized storage structure (by date)
  - Signed URL generation for secure access
  - Duplicate detection via Firestore
  - Metadata tracking in Firestore

## Storage Structure
Files are stored in GCS with the following path structure:
```
uploads/YYYY/MM/DD/[file-hash]/[filename]
```

## Data Storage
- **Google Cloud Storage**: PDF file storage
- **Firestore**: File metadata and hash tracking
  - Collection: `pdf_files`
  - Document ID: File hash
  - Metadata stored:
    - file_name
    - file_size
    - storage_path
    - content_type
    - created_at

## Verification Scripts
- `verify_pdf_service.py`: Test full upload pipeline
- `list_stored_hashes.py`: View stored file metadata
- `verify_uploads.py`: Check GCS uploads 
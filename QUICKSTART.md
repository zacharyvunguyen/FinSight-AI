# FinSight AI Quickstart Guide

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FinSight-AI.git
cd FinSight-AI
```

2. Create and activate virtual environment:
```bash
conda create -n finsight-ai python=3.11
conda activate finsight-ai
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Required Services

1. **Google Cloud Platform**:
   - Create a project
   - Enable BigQuery API
   - Set up a service account with necessary permissions
   - Create a storage bucket

2. **LlamaParse**:
   - Sign up at llamaparse.com
   - Get API key

3. **Pinecone**:
   - Create account at pinecone.io
   - Create an index with dimension=1536 (OpenAI ada-002)

4. **OpenAI**:
   - Get API key for embeddings

## Testing the Pipeline

1. Test PDF extraction:
```bash
python scripts/test_llama_parse.py
```

2. Test storage integration:
```bash
python scripts/test_storage_integration.py
```

3. Verify full pipeline:
```bash
python scripts/verify_storage_pipeline.py
```

## Architecture

1. **Extraction Pipeline**:
   - Uses LlamaParse for PDF extraction
   - Converts unstructured PDFs to structured data

2. **Storage**:
   - BigQuery: Stores raw content and metadata
   - Pinecone: Stores vector embeddings for search

3. **Services**:
   - extraction.py: PDF processing
   - bigquery.py: SQL storage
   - pinecone.py: Vector embeddings

## Prerequisites
1. Python 3.11
2. Anaconda/Miniconda
3. Google Cloud account
4. OpenAI API account
5. Pinecone account

## Setup Steps

1. **Environment Setup**
   ```bash
   conda create -n finsight-ai python=3.11
   conda activate finsight-ai
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Copy `.env.example` to `.env`
   - Set up API keys in `.env`:
     - OPENAI_API_KEY
     - PINECONE_API_KEY
     - GOOGLE_CLOUD_PROJECT

3. **Google Cloud Setup**
   - Create GCP project
   - Enable Required APIs:
     - Cloud Storage API
     - Cloud Firestore API
     - BigQuery API
   - Create service account with required permissions
     - Storage Admin
     - Cloud Datastore User
     - Firebase Admin
   - Download key to `config/keys/`
   - Update GOOGLE_APPLICATION_CREDENTIALS in `.env`

4. **Storage Setup**
   - **Cloud Storage**:
     - Create a new bucket named `finsight-reports-bucket`
     - Set appropriate region (e.g., us-east1)
   - **Firestore**:
     - Create database in Native mode
     - Choose same region as Storage
     - Use default production rules

5. **Pinecone Setup**
   - Create Pinecone account at pinecone.io
   - Create API key from dashboard
   - Note your cloud and region (default: aws, us-east-1)
   - Update PINECONE_* variables in `.env`:
     ```
     PINECONE_API_KEY=your_api_key
     PINECONE_CLOUD=aws
     PINECONE_REGION=us-east-1
     PINECONE_INDEX_NAME=financial-reports
     ```

6. **Verify Setup**
   ```bash
   python scripts/verify_env.py
   python scripts/test_imports.py
   python scripts/setup_gcp.py
   python scripts/setup_pinecone.py
   python scripts/verify_uploads.py
   python scripts/list_stored_hashes.py
   ```

## Testing File Upload
1. Start the FastAPI server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

2. Visit Swagger UI:
   ```
   http://localhost:8000/docs
   ```

3. Test PDF upload:
   - Use the POST `/api/v1/pdf/upload/` endpoint
   - Upload a PDF file
   - Verify upload:
     - Check GCS storage: `scripts/verify_uploads.py`
     - Check Firestore metadata: `scripts/list_stored_hashes.py`

## Troubleshooting
- Ensure all environment variables are set
- Verify service account key location
- Check Google Cloud API enablement:
  - Cloud Storage API
  - Cloud Firestore API
  - BigQuery API
- Verify service account permissions:
  - Storage Admin for GCS
  - Cloud Datastore User for Firestore
  - Firebase Admin for full access

## PDF Processing Setup

1. Get LlamaParse API key from [LlamaIndex Cloud](https://cloud.llamaindex.ai)

2. Add to `.env`:
```bash
LLAMA_CLOUD_API_KEY=your_api_key_here
```

3. Test extraction:
```bash
# Clean up any existing files
python scripts/cleanup_storage.py

# Test PDF processing
python scripts/verify_pdf_service.py
```

4. Monitor processing status:
- Check job status at https://cloud.llamaindex.ai/
- View logs for detailed processing information 
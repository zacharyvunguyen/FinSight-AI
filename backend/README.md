# FinSight AI Backend

## Structure
```
backend/
├── app/
│   ├── api/        # API endpoints
│   ├── core/       # Core configurations
│   ├── models/     # Data models
│   ├── services/   # Business logic
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
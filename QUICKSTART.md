# FinSight AI Quickstart Guide

## Prerequisites
1. Python 3.11
2. Anaconda/Miniconda
3. Google Cloud account
4. OpenAI API account
5. Pinecone account
6. LlamaParse API key

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
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Service Setup

1. **Google Cloud Platform**:
   - Create a project and note the project ID
   - Enable APIs:
     - BigQuery API
     - Cloud Storage API
   - Set up a service account with permissions:
     - BigQuery Admin
     - Storage Admin
   - Download service account key JSON
   - Update GOOGLE_APPLICATION_CREDENTIALS in .env

2. **LlamaParse**:
   - Sign up at cloud.llamaindex.ai
   - Get API key
   - Add LLAMAPARSE_API_KEY to .env

3. **Pinecone**:
   - Create account at pinecone.io
   - Create an index:
     - Dimension: 1536 (OpenAI ada-002)
     - Metric: cosine
   - Add Pinecone credentials to .env

4. **OpenAI**:
   - Get API key from platform.openai.com
   - Add OPENAI_API_KEY to .env

## Testing the Pipeline

1. Verify environment:
```bash
python scripts/verify_env.py
```

2. Test PDF extraction:
```bash
python scripts/test_llama_parse.py
```

3. Test storage integration:
```bash
python scripts/test_storage_integration.py
```

4. Verify full pipeline:
```bash
python scripts/verify_storage_pipeline.py
```

## Architecture

1. **Extraction Pipeline**:
   - Uses LlamaParse for PDF extraction
   - Converts unstructured PDFs to structured data
   - Extracts tables, text, and financial metrics

2. **Storage**:
   - BigQuery: 
     - Stores raw content and metadata
     - Enables SQL querying of financial data
   - Pinecone:
     - Stores vector embeddings
     - Enables semantic search
     - Maintains document relationships

3. **Services**:
   - extraction.py: PDF processing with LlamaParse
   - bigquery.py: Structured data storage
   - pinecone.py: Vector embeddings and search

## Troubleshooting

1. **Common Issues**:
   - Ensure all API keys are correctly set in .env
   - Verify Google Cloud service account permissions
   - Check Pinecone index dimensions match OpenAI embeddings (1536)

2. **Logs**:
   - Check application logs in ./logs
   - Monitor LlamaParse jobs at cloud.llamaindex.ai
   - View BigQuery query history in GCP Console

## Development

1. Start development server:
```bash
uvicorn backend.app.main:app --reload
```

2. Access API documentation:
```
http://localhost:8000/docs
``` 
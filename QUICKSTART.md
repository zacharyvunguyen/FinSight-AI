# Quick Start Guide

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
   - Enable APIs (Storage, BigQuery)
   - Create service account with required permissions
   - Download key to `config/keys/`
   - Update GOOGLE_APPLICATION_CREDENTIALS in `.env`

4. **Pinecone Setup**
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

5. **Verify Setup**
   ```bash
   python scripts/verify_env.py
   python scripts/test_imports.py
   python scripts/setup_gcp.py
   python scripts/setup_pinecone.py
   ```

## Troubleshooting
- Ensure all environment variables are set
- Verify service account key location
- Check Google Cloud API enablement 
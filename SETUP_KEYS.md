# Environment Key Setup Guide

This guide will help you set up all the necessary keys and environment variables for the FinSight-AI project.

## Required Environment Variables

1. **OPENAI_API_KEY**
   - **Description**: API key for accessing OpenAI's GPT-4 services.
   - **How to Obtain**:
     - Sign up or log in to [OpenAI](https://openai.com/).
     - Navigate to the API section and generate a new API key.
   - **Configuration**:
     - Add the key to your `.env` file:
       ```plaintext
       OPENAI_API_KEY=your_openai_api_key
       ```

2. **PINECONE_API_KEY**
   - **Description**: API key for accessing Pinecone's vector database services.
   - **How to Obtain**:
     - Sign up or log in to [Pinecone](https://www.pinecone.io/).
     - Go to the API keys section and create a new key.
   - **Configuration**:
     - Add the key to your `.env` file:
       ```plaintext
       PINECONE_API_KEY=your_pinecone_api_key
       ```

3. **GOOGLE_CLOUD_PROJECT**
   - **Description**: Google Cloud project ID for accessing BigQuery and Cloud Storage.
   - **How to Obtain**:
     - Sign up or log in to [Google Cloud Platform](https://cloud.google.com/).
     - Create a new project or use an existing one.
     - Find the project ID in the project dashboard.
   - **Configuration**:
     - Add the project ID to your `.env` file:
       ```plaintext
       GOOGLE_CLOUD_PROJECT=your_gcp_project_id
       ```

4. **BIGQUERY_DATASET**
   - **Description**: Dataset name in BigQuery where financial data will be stored.
   - **How to Obtain**:
     - Create a new dataset in your Google Cloud BigQuery console.
   - **Configuration**:
     - Add the dataset name to your `.env` file:
       ```plaintext
       BIGQUERY_DATASET=your_bigquery_dataset
       ```

5. **PINECONE_ENVIRONMENT**
   - **Description**: Pinecone environment name for your vector database.
   - **How to Obtain**:
     - Check your Pinecone dashboard for the environment name.
   - **Configuration**:
     - Add the environment name to your `.env` file:
       ```plaintext
       PINECONE_ENVIRONMENT=your_pinecone_environment
       ```

6. **PINECONE_INDEX_NAME**
   - **Description**: Index name in Pinecone for storing vector embeddings.
   - **How to Obtain**:
     - Create a new index in your Pinecone dashboard.
   - **Configuration**:
     - Add the index name to your `.env` file:
       ```plaintext
       PINECONE_INDEX_NAME=your_pinecone_index_name
       ```

## Additional Configuration

- Ensure your `.env` file is located in the root directory of your project.
- Do not commit your `.env` file to version control to keep your keys secure.

## Troubleshooting

- If you encounter issues with any API, ensure your keys are correct and have the necessary permissions.
- Check the respective service's documentation for more detailed setup instructions.

## Google Cloud Platform Setup

1. **Create a GCP Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Note the Project ID

2. **Enable Required APIs**:
   - Cloud Storage API
   - BigQuery API

3. **Create Service Account**:
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Grant required roles:
     - `Storage Admin`
     - `BigQuery Admin`
   - Create and download JSON key file

4. **Configure Environment Variables**:
   ```plaintext
   GOOGLE_CLOUD_PROJECT=your-project-id
   GCP_STORAGE_BUCKET=finsight-reports-bucket
   BIGQUERY_DATASET=financial_analysis
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
   ```

5. **Run Setup Script**:
   ```bash
   python scripts/setup_gcp.py
   ```

## Security Notes
- Store service account key securely
- Never commit credentials to version control
- Use minimal required permissions for service accounts 
from google.cloud import storage, bigquery
from google.api_core import exceptions
import os
from dotenv import load_dotenv

def validate_environment():
    """Validate required environment variables are set."""
    required_vars = {
        'GOOGLE_CLOUD_PROJECT': 'GCP project ID',
        'GCP_STORAGE_BUCKET': 'Cloud Storage bucket name',
        'BIGQUERY_DATASET': 'BigQuery dataset name',
        'GOOGLE_APPLICATION_CREDENTIALS': 'Path to service account key file'
    }
    
    missing_vars = []
    print("\n🔍 Checking environment variables...")
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"- {var}: {description}")
        else:
            print(f"✅ {var} is set")
            
    if missing_vars:
        print("\n❌ Missing required environment variables:")
        print("\n".join(missing_vars))
        print("\nPlease set these variables in your .env file")
        return False
        
    # Verify service account key file exists
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not os.path.exists(creds_path):
        print(f"\n❌ Service account key file not found at: {creds_path}")
        return False
    print(f"✅ Service account key file found")
    
    return True

def setup_gcp_services():
    """Set up GCP services including Storage bucket and BigQuery tables."""
    load_dotenv()
    
    # Validate environment before proceeding
    if not validate_environment():
        return
    
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    bucket_name = os.getenv('GCP_STORAGE_BUCKET')
    dataset_name = os.getenv('BIGQUERY_DATASET')
    
    print("\n🔄 Setting up Google Cloud Services...")
    
    try:
        # Initialize clients
        storage_client = storage.Client()
        bigquery_client = bigquery.Client()
    except Exception as e:
        print(f"\n❌ Failed to initialize Google Cloud clients: {str(e)}")
        print("Please verify your service account credentials and permissions")
        return
    
    # Create Storage Bucket
    try:
        bucket = storage_client.create_bucket(bucket_name)
        print(f"✅ Created Cloud Storage bucket: {bucket.name}")
    except exceptions.Conflict:
        print(f"ℹ️ Bucket {bucket_name} already exists")
    except Exception as e:
        print(f"❌ Error creating bucket: {str(e)}")
    
    # Create BigQuery Dataset
    dataset_id = f"{project_id}.{dataset_name}"
    try:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset = bigquery_client.create_dataset(dataset, exists_ok=True)
        print(f"✅ Created BigQuery dataset: {dataset_id}")
    except Exception as e:
        print(f"❌ Error creating dataset: {str(e)}")
    
    # Create BigQuery Tables
    tables = {
        'financial_reports': """
            CREATE TABLE IF NOT EXISTS `{project}.{dataset}.financial_reports` (
                report_id STRING,
                report_date DATE,
                report_type STRING,
                company_name STRING,
                extracted_data JSON,
                upload_timestamp TIMESTAMP,
                source_file_path STRING
            )
        """,
        'report_comparisons': """
            CREATE TABLE IF NOT EXISTS `{project}.{dataset}.report_comparisons` (
                comparison_id STRING,
                base_report_id STRING,
                compare_report_id STRING,
                comparison_type STRING,
                differences JSON,
                comparison_timestamp TIMESTAMP,
                materiality_threshold FLOAT64
            )
        """
    }
    
    for table_name, schema in tables.items():
        try:
            query = schema.format(project=project_id, dataset=dataset_name)
            query_job = bigquery_client.query(query)
            query_job.result()
            print(f"✅ Created BigQuery table: {table_name}")
        except Exception as e:
            print(f"❌ Error creating table {table_name}: {str(e)}")

if __name__ == "__main__":
    setup_gcp_services() 
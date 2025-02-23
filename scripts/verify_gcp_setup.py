from google.cloud import storage, bigquery
import os
from dotenv import load_dotenv

def verify_gcp_setup():
    load_dotenv()
    
    print("🔍 Verifying GCP Setup...")
    
    # Verify environment variables
    required_vars = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_CLOUD_PROJECT',
        'GCP_STORAGE_BUCKET',
        'BIGQUERY_DATASET'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} is set to: {value}")
        else:
            print(f"❌ {var} is not set")
    
    try:
        # Test Storage access
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets(max_results=1))
        print("✅ Successfully connected to Cloud Storage")
        
        # Test BigQuery access
        bigquery_client = bigquery.Client()
        datasets = list(bigquery_client.list_datasets(max_results=1))
        print("✅ Successfully connected to BigQuery")
        
    except Exception as e:
        print(f"❌ Error testing GCP access: {str(e)}")
        print("Please verify your service account credentials and permissions")

if __name__ == "__main__":
    verify_gcp_setup() 
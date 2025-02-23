from google.cloud import storage
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

def list_uploaded_files():
    """List all uploaded PDFs in the GCS bucket."""
    load_dotenv()
    
    print("\n🔍 Checking uploaded files in GCS...")
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    # Initialize client
    storage_client = storage.Client(
        credentials=credentials,
        project=os.getenv('GOOGLE_CLOUD_PROJECT')
    )
    
    bucket = storage_client.bucket(os.getenv('GCP_STORAGE_BUCKET'))
    
    # List all files in the uploads directory
    blobs = bucket.list_blobs(prefix='uploads/')
    
    print("\nUploaded files:")
    print("-" * 50)
    for blob in blobs:
        print(f"📄 Path: {blob.name}")
        print(f"   Size: {blob.size // 1024} KB")
        print(f"   Created: {blob.time_created}")
        print(f"   URL: {blob.public_url}")
        print("-" * 50)

if __name__ == "__main__":
    list_uploaded_files() 
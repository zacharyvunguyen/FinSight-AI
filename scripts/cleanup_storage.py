from google.cloud import storage, firestore
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

def cleanup_storage():
    """Clean up files from both GCS and Firestore."""
    load_dotenv()
    
    print("\n🧹 Cleaning up storage...")
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    
    # Initialize clients
    storage_client = storage.Client(credentials=credentials)
    firestore_client = firestore.Client(credentials=credentials)
    
    # Clean up GCS
    print("\nCleaning Google Cloud Storage:")
    bucket = storage_client.bucket(os.getenv('GCP_STORAGE_BUCKET'))
    blobs = bucket.list_blobs(prefix='uploads/')
    
    for blob in blobs:
        print(f"Deleting: {blob.name}")
        blob.delete()
    
    # Clean up Firestore
    print("\nCleaning Firestore:")
    docs = firestore_client.collection('pdf_files').stream()
    for doc in docs:
        print(f"Deleting document: {doc.id}")
        doc.reference.delete()
    
    print("\n✨ Cleanup complete!")

if __name__ == "__main__":
    cleanup_storage() 
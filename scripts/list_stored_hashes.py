from google.cloud import firestore
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

def list_stored_hashes(specific_hash=None):
    """List all file hashes stored in Firestore."""
    load_dotenv()
    
    if specific_hash:
        print(f"\n🔍 Checking specific hash: {specific_hash}")
    else:
        print("\n🔍 Listing all stored file hashes...")
    
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    
    db = firestore.Client(
        credentials=credentials,
        project=os.getenv('GOOGLE_CLOUD_PROJECT')
    )
    
    if specific_hash:
        # Check specific hash
        doc = db.collection('pdf_files').document(specific_hash).get()
        if doc.exists:
            data = doc.to_dict()
            print("\nFound matching file:")
            print(f"Filename: {data.get('file_name')}")
            print(f"Upload time: {data.get('extraction_metadata', {}).get('extraction_time')}")
            print(f"Status: {data.get('extraction_metadata', {}).get('status')}")
        else:
            print("No matching file found")
        return
    
    # List all files
    docs = db.collection('pdf_files').stream()
    for doc in docs:
        print(f"\nHash: {doc.id}")
        data = doc.to_dict()
        print(f"Filename: {data.get('file_name')}")
        print(f"Upload time: {data.get('created_at')}")
        print("-" * 50)

if __name__ == "__main__":
    # Check the specific hash from your test
    list_stored_hashes("06a0127e4ca24fc5ad4f5888c7c48839ba1fb89f907d4c98b8fc9077d5fb3929") 
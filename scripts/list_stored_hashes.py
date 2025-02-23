from google.cloud import firestore
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

def list_stored_hashes():
    """List all file hashes stored in Firestore."""
    load_dotenv()
    
    print("\n🔍 Listing stored file hashes...")
    
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    
    db = firestore.Client(
        credentials=credentials,
        project=os.getenv('GOOGLE_CLOUD_PROJECT')
    )
    
    docs = db.collection('pdf_files').stream()
    for doc in docs:
        print(f"\nHash: {doc.id}")
        data = doc.to_dict()
        print(f"Filename: {data.get('file_name')}")
        print(f"Upload time: {data.get('created_at')}")
        print("-" * 50)

if __name__ == "__main__":
    list_stored_hashes() 
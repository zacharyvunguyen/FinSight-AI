import requests
import os
from google.cloud import storage, firestore
from google.oauth2 import service_account
from dotenv import load_dotenv
from datetime import datetime
import hashlib

def verify_pdf_services():
    """Verify PDF upload, storage, metadata and extraction services."""
    load_dotenv()
    
    print("\n🔍 Verifying PDF Services...")
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    # Initialize clients
    storage_client = storage.Client(credentials=credentials)
    firestore_client = firestore.Client(credentials=credentials)
    
    # Test file path
    test_file = "data/test/pdfs/10_09.06.24_0445_BD4_PrelimBook Proj_CY_AugFY25.pdf"
    
    # Verify file exists
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return
    
    print("\n1. Testing PDF Upload & Extraction")
    print("-" * 50)
    try:
        # Upload PDF
        with open(test_file, 'rb') as f:
            sha256_hash = hashlib.sha256()
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            computed_hash = sha256_hash.hexdigest()
            print(f"Computed Hash: {computed_hash}")
            f.seek(0)
            
            files = {'file': (os.path.basename(test_file), f, 'application/pdf')}
            response = requests.post(
                'http://localhost:8000/api/v1/pdf/upload/',
                files=files
            )
        
        if response.status_code == 200:
            print("✅ Upload successful")
            data = response.json()
            print(f"   File Hash: {data['file_hash']}")
            print(f"   Storage Path: {data['storage_path']}")
            print(f"   Signed URL available: {'signed_url' in data}")
            print(f"   Extraction Status: {data['extraction_status']}")
            
            # Store for further tests
            file_hash = data['file_hash']
            storage_path = data['storage_path']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return
            
    except Exception as e:
        print(f"❌ Upload test failed: {str(e)}")
        return
    
    print("\n2. Verifying GCS Storage")
    print("-" * 50)
    try:
        bucket = storage_client.bucket(os.getenv('GCP_STORAGE_BUCKET'))
        blob = bucket.get_blob(storage_path)
        if blob:
            print("✅ File found in GCS")
            print(f"   Size: {blob.size // 1024} KB")
            print(f"   Created: {blob.time_created}")
            print(f"   Content Type: {blob.content_type}")
        else:
            print("❌ File not found in GCS")
            
    except Exception as e:
        print(f"❌ GCS verification failed: {str(e)}")
    
    print("\n3. Verifying Firestore Metadata & Extraction")
    print("-" * 50)
    try:
        doc_ref = firestore_client.collection('pdf_files').document(file_hash)
        doc = doc_ref.get()
        if doc.exists:
            print("✅ Metadata found in Firestore")
            data = doc.to_dict()
            print(f"   Filename: {data.get('file_name')}")
            print(f"   Size: {data.get('file_size')} bytes")
            print(f"   Extraction Status: {data.get('extraction_metadata', {}).get('status')}")
            if data.get('extracted_content'):
                print("   Extracted Content: Available")
                print("   First 200 chars of content:")
                print(f"   {data.get('extracted_content')[:200]}...")
            else:
                print("❌ No extracted content found")
        else:
            print("❌ Metadata not found in Firestore")
            
    except Exception as e:
        print(f"❌ Firestore verification failed: {str(e)}")
    
    print("\n4. Testing Duplicate Detection")
    print("-" * 50)
    try:
        # Try uploading the same file again
        with open(test_file, 'rb') as f:
            files = {'file': (os.path.basename(test_file), f, 'application/pdf')}
            response = requests.post(
                'http://localhost:8000/api/v1/pdf/upload/',
                files=files
            )
        
        if response.status_code == 409:
            print("✅ Duplicate detection working")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Duplicate detection failed")
            print(f"   Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Duplicate test failed: {str(e)}")

if __name__ == "__main__":
    verify_pdf_services() 
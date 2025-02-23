from dotenv import load_dotenv
import os
from backend.app.services.storage import StorageService
from backend.app.services.firestore import FirestoreService
from backend.app.services.extraction import ExtractionService
from backend.app.services.bigquery import BigQueryService
from backend.app.services.pinecone import PineconeService
import hashlib
import time
import asyncio

async def verify_pipeline():
    """Verify the entire storage pipeline."""
    load_dotenv()
    
    print("\n🔍 Verifying Storage Pipeline")
    print("-" * 50)
    
    # Initialize services
    storage_service = StorageService(os.getenv('GCP_STORAGE_BUCKET'))
    firestore_service = FirestoreService()
    extraction_service = ExtractionService()
    bigquery_service = BigQueryService()
    pinecone_service = PineconeService()
    
    # Test file
    test_file = "data/test/pdfs/10_09.06.24_0445_BD4_PrelimBook Proj_CY_AugFY25.pdf"
    
    try:
        print("\n1. File Processing")
        print("-" * 30)
        
        # Read file and compute hash
        with open(test_file, 'rb') as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
            print(f"File hash: {file_hash}")
        
        # Extract data
        extraction_result = await extraction_service.extract_data(
            test_file,
            file_hash
        )
        print(f"Extraction status: {extraction_result['metadata']['status']}")
        
        print("\n2. Storage Verification")
        print("-" * 30)
        
        # Verify BigQuery storage
        print("\nChecking BigQuery:")
        bigquery_service.store_pdf_data(
            file_hash=file_hash,
            file_name=os.path.basename(test_file),
            content=extraction_result['content'],
            extraction_status=extraction_result['metadata']['status'],
            job_id=extraction_result['metadata']['job_id']
        )
        print("✅ Data stored in BigQuery")
        
        # Verify Pinecone storage
        print("\nChecking Pinecone:")
        vector_id = pinecone_service.store_embeddings(
            content=extraction_result['content'],
            metadata={
                'file_hash': file_hash,
                'file_name': os.path.basename(test_file)
            }
        )
        
        # Verify vector storage with retries
        max_retries = 5
        for attempt in range(max_retries):
            time.sleep(2)  # Wait between attempts
            fetch_response = pinecone_service.index.fetch(ids=[vector_id])
            
            if vector_id in fetch_response.vectors:
                vector_data = fetch_response.vectors[vector_id]
                print("✅ Vector stored in Pinecone")
                print(f"Vector dimensions: {len(vector_data.values)}")
                print(f"Metadata: {vector_data.metadata}")
                break
            else:
                print(f"Attempt {attempt + 1}: Waiting for vector to be available...")
        else:
            print("❌ Failed to verify vector in Pinecone")
        
        print("\n✅ Pipeline verification complete!")
        
    except Exception as e:
        print(f"\n❌ Pipeline verification failed:")
        print(f"Error: {str(e)}")
        raise e

if __name__ == "__main__":
    # Run the async function
    asyncio.run(verify_pipeline()) 
from dotenv import load_dotenv
import os
from backend.app.services.bigquery import BigQueryService
from backend.app.services.pinecone import PineconeService
import hashlib
from datetime import datetime
import time

def test_storage_integration():
    """Test BigQuery and Pinecone storage integration."""
    load_dotenv()
    
    print("\n🔍 Testing Storage Integration")
    print("-" * 50)
    
    # Test content
    test_content = """
    # Financial Report Analysis
    
    ## Key Metrics
    - Revenue: $1.2M
    - Profit: $300K
    - Growth: 15%
    
    ## Summary
    This is a test document for storage integration.
    """
    
    # Generate a test hash
    test_hash = hashlib.sha256(test_content.encode()).hexdigest()
    
    try:
        print("\n1. Testing BigQuery Storage")
        print("-" * 30)
        
        bq_service = BigQueryService()
        bq_service.store_pdf_data(
            file_hash=test_hash,
            file_name="test_document.pdf",
            content=test_content,
            extraction_status="success",
            job_id="test-job-123"
        )
        print("✅ Successfully stored in BigQuery")
        
        print("\n2. Testing Pinecone Storage")
        print("-" * 30)
        
        # Verify Pinecone environment variables
        required_vars = [
            'PINECONE_API_KEY',
            'PINECONE_ENVIRONMENT',
            'PINECONE_INDEX_NAME',
            'PINECONE_CLOUD',
            'PINECONE_REGION',
            'OPENAI_API_KEY'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Missing environment variable: {var}")
        
        print("✅ Pinecone environment variables verified")
        
        pinecone_service = PineconeService()
        vector_id = pinecone_service.store_embeddings(
            content=test_content,
            metadata={
                'file_hash': test_hash,
                'file_name': 'test_document.pdf',
                'storage_path': f'uploads/test/{test_hash}/test_document.pdf'
            }
        )
        print(f"✅ Successfully stored in Pinecone with ID: {vector_id}")
        
        # Verify Pinecone storage with retries
        print("\nVerifying Pinecone storage...")
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # Wait before checking
                time.sleep(2)  # Wait 2 seconds between attempts
                
                fetch_response = pinecone_service.index.fetch(ids=[vector_id])
                
                # Check if vector exists in response
                if vector_id in fetch_response.vectors:
                    print("✅ Vector found in Pinecone")
                    vector_data = fetch_response.vectors[vector_id]
                    print(f"Metadata: {vector_data.metadata}")
                    print(f"Vector dimensions: {len(vector_data.values)}")
                    break
                else:
                    print(f"Attempt {attempt + 1}: Vector not found yet, retrying...")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
        else:
            print("❌ Vector not found in Pinecone after all retries")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise e

if __name__ == "__main__":
    test_storage_integration() 
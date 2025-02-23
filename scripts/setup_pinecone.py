import os
import re
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

def validate_index_name(name):
    """Validate index name follows Pinecone naming rules."""
    if not name:
        return False
    # Only allow lowercase alphanumeric and hyphens
    pattern = r'^[a-z0-9-]+$'
    return bool(re.match(pattern, name))

def setup_pinecone():
    """Set up Pinecone index with OpenAI dimensions."""
    load_dotenv()
    
    print("\n🔄 Setting up Pinecone...")
    
    # Verify environment variables
    required_vars = {
        'PINECONE_API_KEY': 'API key for Pinecone',
        'PINECONE_CLOUD': 'Cloud provider (aws)',
        'PINECONE_REGION': 'Region (e.g., us-east-1)',
        'PINECONE_INDEX_NAME': 'Name of the Pinecone index'
    }
    
    # Check for missing variables
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"- {var}: {description}")
        else:
            print(f"✅ {var} is set")
    
    if missing_vars:
        print("\n❌ Missing required environment variables:")
        print("\n".join(missing_vars))
        return False
    
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    index_name = os.getenv('PINECONE_INDEX_NAME')
    
    # Validate index name
    if not validate_index_name(index_name):
        print(f"\n❌ Invalid index name: {index_name}")
        print("Index name must contain only lowercase letters, numbers, and hyphens")
        return False
    
    try:
        # Delete existing index if it exists
        if index_name in pc.list_indexes().names():
            print(f"\n🗑️ Deleting existing index: {index_name}")
            pc.delete_index(index_name)
        
        # Create new index with OpenAI dimensions
        print(f"\n📦 Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI text-embedding-ada-002 dimensions
            metric='cosine',
            spec=ServerlessSpec(
                cloud=os.getenv('PINECONE_CLOUD'),
                region=os.getenv('PINECONE_REGION')
            )
        )
        print("✅ Index created successfully with 1536 dimensions")
        return True
        
    except Exception as e:
        print(f"\n❌ Error setting up Pinecone: {str(e)}")
        return False

if __name__ == "__main__":
    setup_pinecone() 
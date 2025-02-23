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
    """Set up Pinecone index for vector embeddings."""
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
    
    # Validate index name
    index_name = os.getenv('PINECONE_INDEX_NAME')
    if not validate_index_name(index_name):
        print(f"\n❌ Invalid index name: {index_name}")
        print("Index name must contain only lowercase letters, numbers, and hyphens")
        return False
    
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        print("✅ Connected to Pinecone")
        
        # Create index if it doesn't exist
        if index_name not in [index.name for index in pc.list_indexes()]:
            pc.create_index(
                name=index_name,
                dimension=1536,  # OpenAI text-embedding-ada-002 dimensions
                metric='cosine',
                spec=ServerlessSpec(
                    cloud=os.getenv('PINECONE_CLOUD'),
                    region=os.getenv('PINECONE_REGION')
                )
            )
            print(f"✅ Created new index: {index_name}")
        else:
            print(f"ℹ️ Index {index_name} already exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Pinecone: {str(e)}")
        return False

if __name__ == "__main__":
    setup_pinecone() 
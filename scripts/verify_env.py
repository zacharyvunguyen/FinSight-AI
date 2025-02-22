from dotenv import load_dotenv
import os

def verify_environment():
    # Load environment variables
    load_dotenv()
    
    # Required environment variables
    required_vars = [
        'OPENAI_API_KEY',
        'PINECONE_API_KEY',
        'GOOGLE_CLOUD_PROJECT',
        'BIGQUERY_DATASET',
        'PINECONE_ENVIRONMENT',
        'PINECONE_INDEX_NAME'
    ]
    
    # Check each required variable
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease add these variables to your .env file")
    else:
        print("✅ All environment variables are set!")
        
if __name__ == "__main__":
    verify_environment() 
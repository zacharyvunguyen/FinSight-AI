import requests
import os
from dotenv import load_dotenv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

# Increase max pool size
urllib3.PoolManager(maxsize=100)

def create_session():
    """Create requests session with retry logic."""
    session = requests.Session()
    
    # Configure more aggressive retry strategy
    retries = Retry(
        total=10,  # More retries
        backoff_factor=2,  # Exponential backoff
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],  # Allow retries on POST
        raise_on_status=False
    )
    
    # Configure adapter with longer timeouts
    adapter = HTTPAdapter(
        max_retries=retries,
        pool_connections=20,
        pool_maxsize=20,
        pool_block=True
    )
    
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session

def test_llama_parse():
    """Test LlamaParse API directly."""
    load_dotenv()
    
    api_key = os.getenv('LLAMA_CLOUD_API_KEY')
    base_url = "https://api.cloud.llamaindex.ai/api/parsing"
    
    print(f"\n🔑 API Key (first 10 chars): {api_key[:10]}...")
    print(f"🌐 Base URL: {base_url}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    session = create_session()
    
    try:
        print("\n1. Testing file upload...")
        upload_url = f"{base_url}/upload"
        
        test_file = "data/test/pdfs/10_09.06.24_0445_BD4_PrelimBook Proj_CY_AugFY25.pdf"
        print(f"   File: {test_file}")
        
        with open(test_file, 'rb') as f:
            files = {
                'file': (os.path.basename(test_file), f, 'application/pdf')
            }
            
            # Upload with longer timeout
            response = session.post(
                upload_url,
                headers=headers,
                files=files,
                timeout=(30, 90)  # (connect timeout, read timeout)
            )
            print(f"   Upload status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                job_id = response.json()['id']
                print(f"\n2. Checking job status: {job_id}")
                
                # Poll for completion with timeout
                start_time = time.time()
                max_wait_time = 300  # 5 minutes timeout
                
                while (time.time() - start_time) < max_wait_time:
                    try:
                        status_response = session.get(
                            f"{base_url}/job/{job_id}",
                            headers=headers,
                            timeout=(10, 30)
                        )
                        
                        if status_response.status_code != 200:
                            print(f"   Warning: Status check failed with code {status_response.status_code}")
                            time.sleep(10)
                            continue
                            
                        status_data = status_response.json()
                        print(f"   Status: {status_data['status']}")
                        
                        # Check for both COMPLETED and SUCCESS
                        if status_data['status'] in ['COMPLETED', 'SUCCESS']:
                            print("   ✅ Processing complete!")
                            break
                        elif status_data['status'] == 'FAILED':
                            raise Exception(f"Processing failed: {status_data.get('error')}")
                        elif status_data['status'] == 'PENDING':
                            time.sleep(10)
                        else:
                            print(f"   Unknown status: {status_data['status']}")
                            time.sleep(10)
                        
                    except requests.exceptions.RequestException as e:
                        print(f"   Warning: Request failed, retrying... ({str(e)})")
                        time.sleep(10)
                        continue
                    except Exception as e:
                        print(f"   Warning: Unexpected error, retrying... ({str(e)})")
                        time.sleep(10)
                        continue
                else:
                    raise Exception("Processing timeout after 5 minutes")
                
                print("\n3. Getting results...")
                try:
                    result_response = session.get(
                        f"{base_url}/job/{job_id}/result/markdown",
                        headers=headers,
                        timeout=(10, 30)
                    )
                    print(f"   Response status: {result_response.status_code}")
                    print(f"   Raw response: {result_response.text}")  # Print raw response
                    
                    if result_response.status_code == 200:
                        result_data = result_response.json()
                        print(f"   Response data: {result_data}")  # Print parsed JSON
                        
                        # Check response structure
                        if 'markdown' in result_data:  # API might return 'markdown' instead of 'content'
                            content = result_data['markdown']
                        elif 'text' in result_data:    # Or might be 'text'
                            content = result_data['text']
                        elif 'content' in result_data:  # Or 'content'
                            content = result_data['content']
                        else:
                            raise KeyError(f"Could not find content in response: {result_data}")
                            
                        print("   First 200 chars of content:")
                        print(f"   {content[:200]}")
                        return content
                except Exception as e:
                    print(f"   Failed to get results: {str(e)}")
                    print(f"   Error type: {type(e)}")
                    return None
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print(f"   Type: {type(e)}")
        return None

def get_existing_job_results(job_id: str):
    """Get results from an existing successful job."""
    load_dotenv()
    
    api_key = os.getenv('LLAMA_CLOUD_API_KEY')
    base_url = "https://api.cloud.llamaindex.ai/api/parsing"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    session = create_session()
    
    try:
        print(f"\n🔍 Getting results for job: {job_id}")
        
        # Get job status first
        status_response = session.get(
            f"{base_url}/job/{job_id}",
            headers=headers,
            timeout=10
        )
        status_data = status_response.json()
        print(f"Status: {status_data['status']}")
        
        if status_data['status'] == 'COMPLETED':
            # Get markdown results
            result_response = session.get(
                f"{base_url}/job/{job_id}/result/markdown",
                headers=headers,
                timeout=10
            )
            if result_response.status_code == 200:
                content = result_response.json()['content']
                print("\nFirst 200 chars of content:")
                print(f"{content[:200]}")
                return content
            else:
                print(f"Failed to get results: {result_response.text}")
        else:
            print(f"Job not completed. Status: {status_data['status']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    test_llama_parse() 
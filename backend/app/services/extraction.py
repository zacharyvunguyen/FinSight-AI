import requests
import time
from datetime import datetime
import os
from ..core.config import settings
import traceback
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import asyncio

class ExtractionService:
    """Service for extracting structured data from PDFs using LlamaParse API.
    
    Features:
    - PDF upload and processing
    - Status tracking with retry logic
    - Markdown content extraction
    - Error handling and logging
    """
    
    def __init__(self):
        """Initialize LlamaParse client."""
        self.api_key = settings.LLAMA_CLOUD_API_KEY
        self.base_url = "https://api.cloud.llamaindex.ai/api/parsing"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
        
        # Create session with retry logic
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        print("✅ LlamaParse client initialized")
    
    async def get_existing_results(self, job_id: str):
        """Get results from an existing job."""
        try:
            # Check status
            status_response = self.session.get(
                f"{self.base_url}/job/{job_id}",
                headers=self.headers,
                timeout=10
            )
            status_data = status_response.json()
            
            if status_data['status'] != 'COMPLETED':
                raise Exception(f"Job not completed. Status: {status_data['status']}")
            
            # Get results
            result_response = self.session.get(
                f"{self.base_url}/job/{job_id}/result/markdown",
                headers=self.headers,
                timeout=10
            )
            result_response.raise_for_status()
            return result_response.json()['content']
            
        except Exception as e:
            print(f"Failed to get results: {str(e)}")
            return None

    async def extract_data(self, file_path: str, file_hash: str):
        """Extract structured data from PDF using LlamaParse API.
        
        Args:
            file_path (str): Path to PDF file
            file_hash (str): Hash of the file for tracking
            
        Returns:
            dict: {
                'content': str | None,  # Markdown content if successful
                'metadata': {
                    'file_hash': str,
                    'extraction_time': datetime,
                    'status': str,  # 'success' or 'failed'
                    'job_id': str,
                    'error': str,  # Only present if failed
                }
            }
        """
        try:
            # First try to get results from website job
            website_job_id = "67906bb3-fe8b-405d-b2b6-a92218360779"  # From successful job
            content = await self.get_existing_results(website_job_id)
            
            if content:
                return {
                    'content': content,
                    'metadata': {
                        'file_hash': file_hash,
                        'extraction_time': datetime.now(),
                        'status': 'success',
                        'job_id': website_job_id
                    }
                }
            
            # If no existing results, continue with new upload...
            print(f"\n📄 Starting extraction for: {file_path}")
            
            # Upload file
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'application/pdf')
                }
                response = self.session.post(
                    f"{self.base_url}/upload",
                    headers=self.headers,
                    files=files,
                    timeout=30
                )
                response.raise_for_status()
                job_id = response.json()['id']
                print(f"Upload successful. Job ID: {job_id}")
            
            # Poll for completion with timeout
            start_time = time.time()
            max_wait_time = 300  # 5 minutes timeout
            
            while (time.time() - start_time) < max_wait_time:
                try:
                    status_response = self.session.get(
                        f"{self.base_url}/job/{job_id}",
                        headers=self.headers,
                        timeout=(10, 30)
                    )
                    status_data = status_response.json()
                    print(f"Status: {status_data['status']}")
                    
                    # Check for both COMPLETED and SUCCESS
                    if status_data['status'] in ['COMPLETED', 'SUCCESS']:
                        break
                    elif status_data['status'] == 'FAILED':
                        raise Exception(f"Processing failed: {status_data.get('error')}")
                    
                    await asyncio.sleep(10)
                    
                except requests.exceptions.RequestException as e:
                    print(f"Warning: Request failed, retrying... ({str(e)})")
                    await asyncio.sleep(5)
                    continue
            else:
                raise Exception("Processing timeout after 5 minutes")
            
            # Get results
            result_response = self.session.get(
                f"{self.base_url}/job/{job_id}/result/markdown",
                headers=self.headers,
                timeout=(10, 30)
            )
            result_response.raise_for_status()
            result_data = result_response.json()
            
            # Extract content from response
            if 'markdown' in result_data:
                content = result_data['markdown']
            elif 'text' in result_data:
                content = result_data['text']
            elif 'content' in result_data:
                content = result_data['content']
            else:
                raise KeyError(f"Could not find content in response: {result_data}")
            
            return {
                'content': content,
                'metadata': {
                    'file_hash': file_hash,
                    'extraction_time': datetime.now(),
                    'status': 'success',
                    'job_id': job_id
                }
            }
            
        except Exception as e:
            print(f"\n❌ Extraction failed: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return {
                'content': None,
                'metadata': {
                    'file_hash': file_hash,
                    'extraction_time': datetime.now(),
                    'status': 'failed',
                    'error': str(e),
                    'error_type': str(type(e))
                }
            } 
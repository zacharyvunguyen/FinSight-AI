from google.cloud import storage
from google.oauth2 import service_account
import hashlib
from datetime import datetime, timedelta
from typing import BinaryIO, Tuple
import os
from ..core.config import settings

class StorageService:
    def __init__(self, bucket_name: str):
        # Load credentials from the service account file
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_APPLICATION_CREDENTIALS,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Initialize storage client with credentials
        self.storage_client = storage.Client(
            credentials=credentials,
            project=settings.GOOGLE_CLOUD_PROJECT
        )
        self.bucket = self.storage_client.bucket(bucket_name)
    
    def compute_file_hash(self, file: BinaryIO) -> str:
        """Compute SHA-256 hash of file content."""
        sha256_hash = hashlib.sha256()
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        file.seek(0)  # Reset file pointer
        return sha256_hash.hexdigest()
    
    def upload_file(self, file: BinaryIO, file_name: str) -> Tuple[str, str]:
        """Upload file to GCS and return storage path and file hash."""
        file_hash = self.compute_file_hash(file)
        
        # Create path with date prefix for better organization
        date_prefix = datetime.now().strftime("%Y/%m/%d")
        storage_path = f"uploads/{date_prefix}/{file_hash}/{file_name}"
        
        blob = self.bucket.blob(storage_path)
        blob.upload_from_file(file)
        
        return storage_path, file_hash
    
    def generate_signed_url(self, storage_path: str, expiration_minutes: int = 30) -> str:
        """Generate signed URL for file access."""
        blob = self.bucket.blob(storage_path)
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET"
        )
        return url 
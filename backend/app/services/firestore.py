from google.cloud import firestore
from google.oauth2 import service_account
from datetime import datetime
from ..core.config import settings

class FirestoreService:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_APPLICATION_CREDENTIALS
        )
        self.db = firestore.Client(
            credentials=credentials,
            project=settings.GOOGLE_CLOUD_PROJECT
        )
    
    async def check_duplicate(self, file_hash: str) -> bool:
        """Check if file hash already exists."""
        doc_ref = self.db.collection('pdf_files').document(file_hash)
        doc = doc_ref.get()
        return doc.exists
    
    async def store_file_metadata(self, file_hash: str, metadata: dict):
        """Store file metadata in Firestore."""
        doc_ref = self.db.collection('pdf_files').document(file_hash)
        metadata['created_at'] = datetime.now()
        doc_ref.set(metadata) 
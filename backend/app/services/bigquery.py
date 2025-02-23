from google.cloud import bigquery
from datetime import datetime
from ..core.config import settings

class BigQueryService:
    """Store structured financial data in BigQuery."""
    
    def __init__(self):
        """Initialize BigQuery client."""
        self.client = bigquery.Client()
        self.dataset_id = settings.BIGQUERY_DATASET
        
        # Ensure dataset exists
        self._create_dataset_if_not_exists()
        # Create tables if they don't exist
        self._create_tables_if_not_exists()
    
    def _create_dataset_if_not_exists(self):
        """Create dataset if it doesn't exist."""
        dataset_ref = self.client.dataset(self.dataset_id)
        try:
            self.client.get_dataset(dataset_ref)
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset)
    
    def _create_tables_if_not_exists(self):
        """Create required tables if they don't exist."""
        dataset_ref = self.client.dataset(self.dataset_id)
        
        # PDF Documents table
        pdf_docs_schema = [
            bigquery.SchemaField("file_hash", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("file_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("upload_timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("content", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("extraction_status", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
        ]
        
        table_ref = dataset_ref.table("pdf_documents")
        try:
            self.client.get_table(table_ref)
        except Exception:
            table = bigquery.Table(table_ref, schema=pdf_docs_schema)
            self.client.create_table(table)
    
    def store_pdf_data(self, file_hash: str, file_name: str, content: str, 
                      extraction_status: str, job_id: str):
        """Store PDF document data in BigQuery."""
        table_id = f"{settings.GOOGLE_CLOUD_PROJECT}.{self.dataset_id}.pdf_documents"
        
        # Convert datetime to RFC 3339 format
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        rows_to_insert = [{
            "file_hash": file_hash,
            "file_name": file_name,
            "upload_timestamp": current_time,  # Use formatted string
            "content": content,
            "extraction_status": extraction_status,
            "job_id": job_id
        }]
        
        errors = self.client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            raise Exception(f"Failed to insert rows: {errors}")
        
        return True

    def store_financial_data(self, structured_data: dict):
        # Store in appropriate tables
        pass 
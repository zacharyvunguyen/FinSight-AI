from .bigquery import BigQueryService
from .pinecone import PineconeService
from openai import OpenAI
from ..core.config import settings
from typing import List, Dict

class SearchService:
    """Service for searching financial data."""
    
    def __init__(self):
        self.bigquery = BigQueryService()
        self.pinecone = PineconeService()
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search using vector similarity."""
        # Generate query embedding
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response.data[0].embedding
        
        # Search Pinecone
        search_response = self.pinecone.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        results = []
        for match in search_response.matches:
            # Get full document from BigQuery
            doc = self.bigquery.get_document(match.metadata['file_hash'])
            if doc:
                results.append({
                    'file_hash': match.metadata['file_hash'],
                    'file_name': match.metadata['file_name'],
                    'score': match.score,
                    'content': doc['content'],
                    'section_type': match.metadata.get('section_type', 'unknown'),
                    'key_metrics': match.metadata.get('key_metrics', {})
                })
        
        return results
    
    async def sql_analysis(self, query: str) -> List[Dict]:
        """Run SQL analysis on financial data."""
        # Add query validation and sanitization
        if not query.lower().startswith('select'):
            raise ValueError("Only SELECT queries are allowed")
        
        return self.bigquery.execute_query(query)
    
    async def search_by_metric(self, metric: str, min_value: float = None, max_value: float = None) -> List[Dict]:
        """Search for documents by financial metric."""
        query = f"""
        SELECT file_hash, file_name, content, upload_timestamp
        FROM `{settings.GOOGLE_CLOUD_PROJECT}.{self.bigquery.dataset_id}.pdf_documents`
        WHERE REGEXP_CONTAINS(content, r'\\${metric}\\s*[0-9,.]+[MBK]?')
        """
        
        if min_value is not None:
            query += f" AND CAST(REGEXP_EXTRACT(content, r'\\${metric}\\s*([0-9,.]+)') AS FLOAT64) >= {min_value}"
        if max_value is not None:
            query += f" AND CAST(REGEXP_EXTRACT(content, r'\\${metric}\\s*([0-9,.]+)') AS FLOAT64) <= {max_value}"
        
        return self.bigquery.execute_query(query) 
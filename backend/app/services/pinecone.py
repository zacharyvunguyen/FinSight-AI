from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from ..core.config import settings
import uuid
import tiktoken

class PineconeService:
    """Store vector embeddings for financial data."""
    
    def __init__(self):
        """Initialize Pinecone and OpenAI clients."""
        # Initialize Pinecone
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Initialize tokenizer
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")
        
        # Get or create index
        if settings.PINECONE_INDEX_NAME not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=1536,  # OpenAI text-embedding-ada-002 dimensions
                metric='cosine',
                spec=ServerlessSpec(
                    cloud=settings.PINECONE_CLOUD,
                    region=settings.PINECONE_REGION
                )
            )
        
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        print("✅ Pinecone and OpenAI clients initialized")
    
    def _chunk_text(self, text: str, max_tokens: int = 8000) -> list[dict]:
        """Split text into meaningful financial chunks."""
        # Split into sections first (using common financial document markers)
        sections = []
        current_section = []
        lines = text.split('\n')
        
        section_markers = [
            'BALANCE SHEET', 'INCOME STATEMENT', 'CASH FLOW',
            'FINANCIAL HIGHLIGHTS', 'REVENUE', 'EXPENSES',
            'OPERATIONS', 'ANALYSIS', 'SUMMARY'
        ]
        
        for line in lines:
            # Start new section if we hit a marker
            if any(marker in line.upper() for marker in section_markers):
                if current_section:
                    sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)
        
        # Add final section
        if current_section:
            sections.append('\n'.join(current_section))
        
        chunks = []
        for section in sections:
            # Skip empty sections
            if not section.strip():
                continue
            
            # Get token count
            tokens = self.tokenizer.encode(section)
            if len(tokens) > max_tokens:
                # If section too large, split by paragraphs
                paras = [p.strip() for p in section.split('\n\n') if p.strip()]
                current_chunk = []
                current_size = 0
                
                for para in paras:
                    para_size = len(self.tokenizer.encode(para))
                    if current_size + para_size > max_tokens and current_chunk:
                        # Store chunk with metadata
                        chunks.append({
                            'text': '\n\n'.join(current_chunk),
                            'section_type': self._identify_section_type(current_chunk[0]),
                            'contains_tables': bool(self._extract_table_data('\n'.join(current_chunk))),
                            'key_metrics': self._extract_key_metrics('\n'.join(current_chunk))
                        })
                        current_chunk = [para]
                        current_size = para_size
                    else:
                        current_chunk.append(para)
                        current_size += para_size
                
                if current_chunk:
                    chunks.append({
                        'text': '\n\n'.join(current_chunk),
                        'section_type': self._identify_section_type(current_chunk[0]),
                        'contains_tables': bool(self._extract_table_data('\n'.join(current_chunk))),
                        'key_metrics': self._extract_key_metrics('\n'.join(current_chunk))
                    })
            else:
                # Store whole section as one chunk
                chunks.append({
                    'text': section,
                    'section_type': self._identify_section_type(section),
                    'contains_tables': bool(self._extract_table_data(section)),
                    'key_metrics': self._extract_key_metrics(section)
                })
        
        return chunks
    
    def _identify_section_type(self, text: str) -> str:
        """Identify the type of financial section."""
        text = text.upper()
        if 'BALANCE SHEET' in text:
            return 'balance_sheet'
        elif 'INCOME STATEMENT' in text:
            return 'income_statement'
        elif 'CASH FLOW' in text:
            return 'cash_flow'
        elif 'REVENUE' in text or 'SALES' in text:
            return 'revenue'
        elif 'EXPENSES' in text or 'COSTS' in text:
            return 'expenses'
        elif 'OPERATIONS' in text:
            return 'operations'
        elif 'ANALYSIS' in text:
            return 'analysis'
        return 'other'
    
    def _extract_table_data(self, text: str) -> dict:
        """Extract any tabular financial data."""
        # Simple table detection
        if '|' in text or '\t' in text:
            return {'has_tables': True}
        return {}
    
    def _extract_key_metrics(self, text: str) -> dict:
        """Extract key financial metrics from text."""
        metrics = {}
        # Look for currency amounts
        import re
        currency_pattern = r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?(?:\s*[mMbBkK]illion)?'
        amounts = re.findall(currency_pattern, text)
        if amounts:
            metrics['currency_amounts'] = amounts[:5]  # Store up to 5 amounts
        return metrics
    
    def store_embeddings(self, content: str, metadata: dict):
        """Generate and store embeddings in Pinecone."""
        try:
            # Split content into chunks
            chunks = self._chunk_text(content)
            print(f"Split content into {len(chunks)} chunks")
            
            vector_ids = []
            for i, chunk in enumerate(chunks):
                # Generate embedding using OpenAI
                response = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=chunk['text']
                )
                embedding = response.data[0].embedding
                
                # Create vector ID for this chunk
                vector_id = f"{str(uuid.uuid4())}_chunk_{i}"
                vector_ids.append(vector_id)
                
                # Enhanced metadata
                chunk_metadata = {
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'start_text': chunk['text'][:100],
                    'end_text': chunk['text'][-100:],
                    'chunk_size': len(self.tokenizer.encode(chunk['text']))
                }
                
                # Upsert to Pinecone
                upsert_response = self.index.upsert(
                    vectors=[(vector_id, embedding, chunk_metadata)]
                )
                
                # Verify upsert was successful
                if hasattr(upsert_response, 'upserted_count') and upsert_response.upserted_count == 1:
                    print(f"✅ Chunk {i+1}/{len(chunks)} stored successfully")
                    print(f"   Preview: {chunk['text'][:100]}...")
                else:
                    print(f"⚠️ Warning: Upsert response for chunk {i+1}: {upsert_response}")
            
            return vector_ids[0]  # Return first chunk's ID for verification
            
        except Exception as e:
            print(f"Error storing embeddings: {str(e)}")
            raise e 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PDFResponse(BaseModel):
    file_name: str
    file_hash: str
    upload_timestamp: datetime
    file_size: int
    storage_path: str
    signed_url: Optional[str] = None

class PDFStatus(BaseModel):
    file_hash: str
    status: str
    message: str 
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    extracted_data: Optional[Dict[str, Any]] = None
    validation_errors: Optional[List[Any]] = None

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 10
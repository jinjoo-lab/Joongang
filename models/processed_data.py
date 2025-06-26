from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProcessedData(BaseModel):
    id: str
    name: str
    value: float
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None 
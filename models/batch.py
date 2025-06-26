from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BatchResult(BaseModel):
    batch_id: str
    total_processed: int
    success_count: int
    error_count: int
    start_time: datetime
    end_time: Optional[datetime] = None
    errors: List[str] = [] 
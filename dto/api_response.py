from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now() 
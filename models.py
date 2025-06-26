from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class APIResponse(BaseModel):
    """API 응답 기본 모델"""
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()

class BatchResult(BaseModel):
    """배치 처리 결과 모델"""
    batch_id: str
    total_processed: int
    success_count: int
    error_count: int
    start_time: datetime
    end_time: Optional[datetime] = None
    errors: List[str] = []

class ProcessedData(BaseModel):
    """처리된 데이터 모델 (예시)"""
    id: str
    name: str
    value: float
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None 
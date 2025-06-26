import requests
import time
from typing import Dict, Any, Optional
from config import Config
from models import APIResponse

class APIClient:
    
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.api_key = Config.X_API_KEY
        self.timeout = Config.API_TIMEOUT
        self.retry_count = Config.RETRY_COUNT
        self.retry_delay = Config.RETRY_DELAY
        
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
    
    def _make_request(self, method: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        
        url = self.base_url
        for attempt in range(self.retry_count + 1):
            try:
                print(f"API 요청 시도 {attempt + 1}/{self.retry_count + 1}: {method} {url}")
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    timeout=self.timeout,
                    params=params,
                    **kwargs
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < self.retry_count:
                    print(f"⏳ {self.retry_delay}초 후 재시도...")
                    time.sleep(self.retry_delay)
                else:
                    raise
    
    def get_joongang_data(self, ty: str, tm: str, td: str) -> APIResponse:
        
        try:
            params = {
                "ty": ty,  # 년 (yyyy)
                "tm": tm,  # 월 (mm)
                "td": td   # 일 (dd)
            }

            response = self._make_request("GET", params=params)
            data = response.json()
            return APIResponse(
                success=True,
                data=data,
                message="중앙일보 AI 데이터 조회 성공"
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"중앙일보 AI 데이터 조회 실패: {str(e)}"
            )
    
    def get_data(self, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        try:
            response = self._make_request("GET", params=params)
            data = response.json()
            
            return APIResponse(
                success=True,
                data=data,
                message="데이터 조회 성공"
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"데이터 조회 실패: {str(e)}"
            )

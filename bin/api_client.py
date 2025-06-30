import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from typing import Dict, Any, Optional
from conf.config import Config
from dto.api_response import APIResponse
from dto.joongang_response import JoongangAPIResponse

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
            
            # 응답 데이터 검증
            try:
                joongang_response = JoongangAPIResponse(**data)
                return APIResponse(
                    success=True,
                    data=data,
                    message=f"중앙일보 AI 데이터 조회 성공 - {joongang_response.count}개 기사"
                )
            except Exception as validation_error:
                return APIResponse(
                    success=False,
                    message=f"응답 데이터 검증 실패: {str(validation_error)}"
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

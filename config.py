import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:    
    # API 설정
    API_BASE_URL = os.getenv("API_BASE_URL", "https://lima.joongang.co.kr")
    X_API_KEY = os.getenv("X-API-KEY", "")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    
    # 재시도 설정
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5")) 
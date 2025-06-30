#!/usr/bin/env python3
"""
매일 자정에 실행되어 바로 전날 데이터를 수집하고 저장
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from datetime import datetime, timedelta
from pathlib import Path
from bin.api_client import APIClient
from bin.data_service import DataService
from conf.config import Config

# 로깅 설정
def setup_logging():
    """로깅 설정"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    daily_log_file = log_dir / f"joongang_{date_str}.log"
    all_log_file = log_dir / "joongang.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(daily_log_file, encoding='utf-8'),
            logging.FileHandler(all_log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_target_date():
    now = datetime.now()
    target_date = now - timedelta(days=1)
    return target_date

def run_batch_job():
    """배치 작업 실행"""
    try:
        # 로깅 설정
        setup_logging()
        
        # 수집할 날짜 계산
        target_date = get_target_date()
        year = str(target_date.year)
        month = str(target_date.month).zfill(2)
        day = str(target_date.day).zfill(2)
        
        logging.info(f"배치 작업 시작: {year}-{month}-{day}")
        
        # API 클라이언트 및 데이터 서비스 초기화
        api_client = APIClient()
        data_service = DataService()
        
        # API 호출
        logging.info("중앙일보 API 호출 중...")
        response = api_client.get_joongang_data(year, month, day)
        
        if response.success:
            # 데이터 저장
            logging.info("데이터 저장 중...")
            save_result = data_service.save_api_response(year, month, day, response.data)
            
            if save_result:
                logging.info(f"배치 작업 완료: {response.data.get('count', 0)}개 기사 수집")
            else:
                logging.error("데이터 저장 실패")
                return False
        else:
            logging.error(f"API 호출 실패: {response.message}")
            return False
            
        return True
        
    except Exception as e:
        logging.error(f"배치 작업 중 예상치 못한 오류: {str(e)}")
        return False

def main():
    success = run_batch_job()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 
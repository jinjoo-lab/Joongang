import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import logging

class DataService:
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def _create_directory_structure(self, year: str, month: str) -> Path:
        year_dir = self.base_dir / year
        month_dir = year_dir / month.zfill(2)
        
        year_dir.mkdir(exist_ok=True)
        month_dir.mkdir(exist_ok=True)
        
        return month_dir
    
    def _get_file_path(self, year: str, month: str, day: str) -> Path:
        """파일 경로 생성 (DL_DATE=YYYYMMDD/Joongang_YYYYMMDD.json)"""
        # 타겟 날짜 계산
        from datetime import timedelta
        target_date = datetime(int(year), int(month), int(day))
        
        # 디렉토리는 타겟 날짜 + 1일로 생성
        next_day = target_date + timedelta(days=1)
        next_day_str = next_day.strftime('%Y%m%d')
        dir_path = self.base_dir / f"DL_DATE={next_day_str}"
        dir_path.mkdir(exist_ok=True)
        
        # 파일명은 타겟 날짜로 생성
        yyyymmdd = f"{year}{month.zfill(2)}{day.zfill(2)}"
        filename = f"Joongang_{yyyymmdd}.json"
        return dir_path / filename
    
    def save_api_response(self, year: str, month: str, day: str, data: Dict[str, Any]) -> bool:
        try:
            file_path = self._get_file_path(year, month, day)

            # 파일이 이미 있으면 삭제
            if file_path.exists():
                file_path.unlink()

            # JSON 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            return False
    
    def load_api_response(self, year: str, month: str, day: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self._get_file_path(year, month, day)
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            return None
    
    def list_saved_files(self, year: Optional[str] = None, month: Optional[str] = None) -> list:
        files = []
        
        if year:
            year_dir = self.base_dir / year
            if not year_dir.exists():
                return files
            
            if month:
                month_dir = year_dir / month.zfill(2)
                if month_dir.exists():
                    files.extend([f for f in month_dir.glob("*.json")])
            else:
                for month_dir in year_dir.iterdir():
                    if month_dir.is_dir():
                        files.extend([f for f in month_dir.glob("*.json")])
        else:
            for year_dir in self.base_dir.iterdir():
                if year_dir.is_dir():
                    for month_dir in year_dir.iterdir():
                        if month_dir.is_dir():
                            files.extend([f for f in month_dir.glob("*.json")])
        
        return sorted(files)
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        stat = file_path.stat()
        return {
            "path": str(file_path),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "created": datetime.fromtimestamp(stat.st_ctime)
        }

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
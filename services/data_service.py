import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class DataService:
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def _create_directory_structure(self, year: str, month: str) -> Path:
        """년/월 디렉토리 구조 생성"""
        year_dir = self.base_dir / year
        month_dir = year_dir / month.zfill(2)
        
        year_dir.mkdir(exist_ok=True)
        month_dir.mkdir(exist_ok=True)
        
        return month_dir
    
    def _get_file_path(self, year: str, month: str, day: str) -> Path:
        """파일 경로 생성"""
        month_dir = self._create_directory_structure(year, month)
        filename = f"{year}-{month.zfill(2)}-{day.zfill(2)}.json"
        return month_dir / filename
    
    def save_api_response(self, year: str, month: str, day: str, data: Dict[str, Any]) -> bool:
        """API 응답을 JSON 파일로 저장"""
        try:
            file_path = self._get_file_path(year, month, day)
            
            # 파일이 이미 존재하는지 확인
            if file_path.exists():
                print(f"⚠️ 파일이 이미 존재합니다: {file_path}")
                return False
            
            # JSON 파일로 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 데이터 저장 완료: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ 데이터 저장 실패: {str(e)}")
            return False
    
    def load_api_response(self, year: str, month: str, day: str) -> Optional[Dict[str, Any]]:
        """저장된 JSON 파일에서 데이터 로드"""
        try:
            file_path = self._get_file_path(year, month, day)
            
            if not file_path.exists():
                print(f"❌ 파일이 존재하지 않습니다: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ 데이터 로드 완료: {file_path}")
            return data
            
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {str(e)}")
            return None
    
    def list_saved_files(self, year: Optional[str] = None, month: Optional[str] = None) -> list:
        """저장된 파일 목록 조회"""
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
        """파일 정보 조회"""
        stat = file_path.stat()
        return {
            "path": str(file_path),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "created": datetime.fromtimestamp(stat.st_ctime)
        } 
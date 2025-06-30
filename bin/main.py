import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import json
from conf.config import Config
from bin.api_client import APIClient
from bin.data_service import DataService

def main():
    parser = argparse.ArgumentParser(description="중앙일보 AI 데이터 API 호출 테스트 프로그램")
    parser.add_argument("--ty", required=True, help="년도 (yyyy)")
    parser.add_argument("--tm", required=True, help="월 (mm)")
    parser.add_argument("--td", required=True, help="일 (dd)")
    parser.add_argument("--format", choices=["json", "summary"], default="json", help="출력 형식 (json 또는 summary)")
    parser.add_argument("--save", action="store_true", help="API 응답을 JSON 파일로 저장")
    parser.add_argument("--load", action="store_true", help="저장된 JSON 파일에서 데이터 로드")
    parser.add_argument("--list", action="store_true", help="저장된 파일 목록 조회")
    args = parser.parse_args()

    year = args.ty
    month = args.tm
    day = args.td
    output_format = args.format
    save_data = args.save
    load_data = args.load
    list_files = args.list

    data_service = DataService()

    try:
        if list_files:
            files = data_service.list_saved_files()
            if not files:
                print("저장된 파일이 없습니다.")
            else:
                for file_path in files:
                    info = data_service.get_file_info(file_path)
                    print(f"{info['path']} ({info['size']} bytes)")
            return

        if load_data:
            print(f"저장된 데이터 로드 중: {year}년 {month}월 {day}일")
            data = data_service.load_api_response(year, month, day)
            if data is None:
                sys.exit(1)
        else:
            print(f"{year}년 {month}월 {day}일 중앙일보 AI 데이터 조회 중...")
            
            api_client = APIClient()
            response = api_client.get_joongang_data(year, month, day)

            if not response.success:
                print(f"{response.message}")
                sys.exit(1)
            
            data = response.data

            if save_data:
                print(f"데이터 저장 중...")
                if data_service.save_api_response(year, month, day, data):
                    print(f"저장 완료!")
                else:
                    print(f"저장 실패 또는 파일이 이미 존재합니다.")
            
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main() 
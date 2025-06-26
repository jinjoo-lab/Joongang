import sys
import argparse
import json
from config import Config
from api_client import APIClient

def main():
    parser = argparse.ArgumentParser(description="중앙일보 AI 데이터 API 호출 테스트 프로그램")
    parser.add_argument("--ty", required=True, help="년도 (yyyy)")
    parser.add_argument("--tm", required=True, help="월 (mm)")
    parser.add_argument("--td", required=True, help="일 (dd)")
    args = parser.parse_args()

    year = args.ty
    month = args.tm
    day = args.td

    try:
        if int(year) < 2024:
            sys.exit(1)

        api_client = APIClient()
        response = api_client.get_joongang_data(year, month, day)

        if response.success:
            print(json.dumps(response.data, indent=2, ensure_ascii=False))
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main() 
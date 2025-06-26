import sys
import argparse
import json
from config import Config
from api_client import APIClient
from services.data_service import DataService

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
            print("📁 저장된 파일 목록:")
            files = data_service.list_saved_files()
            if not files:
                print("  저장된 파일이 없습니다.")
            else:
                for file_path in files:
                    info = data_service.get_file_info(file_path)
                    print(f"  📄 {info['path']} ({info['size']} bytes)")
            return

        if int(year) < 2024:
            print("❌ 2024년 이후 데이터만 조회 가능합니다.")
            sys.exit(1)

        if load_data:
            print(f"📂 저장된 데이터 로드 중: {year}년 {month}월 {day}일")
            data = data_service.load_api_response(year, month, day)
            if data is None:
                sys.exit(1)
        else:
            print(f"📅 {year}년 {month}월 {day}일 중앙일보 AI 데이터 조회 중...")
            
            api_client = APIClient()
            response = api_client.get_joongang_data(year, month, day)

            if not response.success:
                print(f"❌ {response.message}")
                sys.exit(1)
            
            data = response.data

            if save_data:
                print(f"💾 데이터 저장 중...")
                if data_service.save_api_response(year, month, day, data):
                    print(f"✅ 저장 완료!")
                else:
                    print(f"⚠️ 저장 실패 또는 파일이 이미 존재합니다.")

        if output_format == "json":
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"\n✅ 데이터 조회 성공")
            print(f"📊 총 기사 수: {data.get('count', 0)}개")
            print(f"📅 조회 날짜: {data.get('year')}년 {data.get('month')}월 {data.get('day')}일")
            
            if data.get('articles'):
                print(f"\n📰 기사 목록:")
                for i, article in enumerate(data['articles'][:5], 1):
                    print(f"  {i}. {article.get('title', '제목 없음')}")
                    print(f"     카테고리: {', '.join(article.get('categories', []))}")
                    print(f"     해시태그: {', '.join(article.get('hash_tags', [])[:3])}...")
                    print()
                
                if len(data['articles']) > 5:
                    print(f"  ... 외 {len(data['articles']) - 5}개 기사 더 있음")

    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
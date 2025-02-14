from scraper import scrape_all
from data_parser import parse_data
from save_data import save_to_json
from config import URLS

if __name__ == "__main__":
    print("🚀 크롤링 시작...")
    data = scrape_all(URLS)
    
    print("📌 데이터 정리 중...")
    parsed_data = parse_data(data)

    print("💾 데이터 저장 중...")
    save_to_json(parsed_data)

    print("✅ 크롤링 완료!")

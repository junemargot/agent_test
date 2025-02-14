# HTML 데이터 파싱 - 추출 데이터 가공
import time
import logging
import re
from config import URLS, CHROME_OPTIONS

# 로그 설정
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def clean_text(text):
    """불필요한 텍스트 제거 및 정리"""
    # 로그인, 메뉴, 사이트 공통 요소 제거
    text = re.sub(r'로그인\s*\|*\s*회원가입', '', text)
    text = re.sub(r'탑골이야기|노인복지|지역사회복지|후원/자원봉사|부설센터|기관소개', '', text)
    text = re.sub(r'주소\s*:\s*\d{5}\s*서울.*?\d{2,4}-\d{3,4}-\d{4}', '', text)
    text = re.sub(r'Copyright.*?reserved\.', '', text)
    # 연속 공백 및 개행 정리
    text = re.sub(r'\n+', '\n', text).strip()
    return text

def categorize_data(url):
    """URL 기반으로 데이터를 카테고리화"""
    # if url == "life":
    #     return "생활"
    # elif url == "health":
    #     return "건강지원"
    # elif url == "health2":
    #     return "기능회복서비스"
    # elif url == "culture1":
    #     return "평생교육"
    # elif url == "culture4":
    #     return "동아리"

    if "life" in url:
        return "생활"
    elif "health" in url:
        return "건강지원"
    elif "health2" in url:
        return "기능회복서비스"
    elif "culture1" in url:
        return "평생교육"
    elif "culture4" in url:
        return "동아리"
    else:
        return "기타"
    

def extract_details(description, sub_board):
    """본문을 분석하여 주요 내용을 정리"""
    lines = description.split("\n")
    
    # 제목이 없을 경우 첫 번째 줄을 제목으로 설정
    title = lines[0] if lines and len(lines[0]) > 5 else "제목 없음"
    
    # 일정 정보 추출 (예: 날짜 패턴)
    schedule = [line for line in lines if re.search(r'\d{4}년|\d{1,2}월|\d{1,2}일', line)]

    # 문의처 추출 (전화번호 또는 이메일)
    contact = [line for line in lines if re.search(r'\d{2,4}-\d{3,4}-\d{4}|@', line)]
    
    # 핵심 내용 (나머지 정보)
    main_content = "\n".join(lines[1:]) if len(lines) > 1 else "내용 없음"

    return title, schedule, contact, main_content, clean_text(sub_board)


def parse_data(data):
    """크롤링 데이터 정리 및 카테고리화"""
    cleaned_data = []

    for item in data:
        url = item.get("URL", "")
        category = categorize_data(url)  # 기존 코드 유지
        description = clean_text(item.get("설명", ""))
        sub_board = clean_text(item.get("추가정보", ""))

        # 상세 정보 추출
        title, schedule, contact, main_content, additional_info = extract_details(description, sub_board)

        cleaned_item = {
            "카테고리": category,
            "URL": url,
            "제목": title,
            "주요 내용": main_content,
            "추가 정보": additional_info,
            "일정": schedule if schedule else "일정 정보 없음",
            "문의처": contact if contact else "연락처 정보 없음",
        }
        cleaned_data.append(cleaned_item)

    return cleaned_data

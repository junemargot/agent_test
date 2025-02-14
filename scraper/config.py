# 설정파일

# 크롤링할 URL 리스트
URLS = [
    "https://seoulnoin.or.kr/senior/life.asp", # 경로급식
    "https://seoulnoin.or.kr/senior/life2.asp", # 식단표(월별)
    "https://seoulnoin.or.kr/health.asp", # 건강지원서비스
    "https://seoulnoin.or.kr/senior/health2.asp", # 기능회복서비스
    "https://seoulnoin.or.kr/senior/health3.asp", # 건강증진서비스
    "https://seoulnoin.or.kr/senior/culture1.asp", # 평생교육
    "https://seoulnoin.or.kr/senior/culture6.asp", # 정보화교육
    "https://seoulnoin.or.kr/senior/culture3.asp", # 취미자율이용
    "https://seoulnoin.or.kr/senior/culture4.asp", # 동아리
    "https://seoulnoin.or.kr/senior/work3.asp" # 노인사회활동지원
    "https://seoulnoin.or.kr/senior/work5.asp" # 노인자원봉사
]

CHROME_OPTIONS = [
    "--headless",  # GUI 없이 실행
    "--disable-gpu",
    "--window-size=1920x1080",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

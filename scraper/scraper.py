# 웹 크롤러 - Selenium을 사용해 웹 페이지 가져오기
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from config import URLS, CHROME_OPTIONS

# logs 폴더가 없는 경우 생성
os.makedirs("logs", exist_ok=True)

# 로그 설정
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# 웹 드라이버 설정
def get_driver():
    """Selenium 웹 드라이버 설정"""
    options = Options()
    options.add_argument("--headless") # 화면 없이 실행
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

# 페이지 크롤링 (지정 태그만 가져오기)
def scrape_page(driver, url):
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기

    # 제목 추출
    try:
        title = driver.find_element(By.CSS_SELECTOR, ".contents_wrap h3").text.strip()
    except:
        title = "제목 없음"

    # 카테고리 추출
    try:
        category = driver.find_element(By.CSS_SELECTOR, ".sub_tab3.no_sub li a").text.strip()
    except:
        category = "카테고리 없음"

    # 설명 추출
    try:
        description = driver.find_element(By.CSS_SELECTOR, ".sub_body").text.strip()
    except:
        description = "설명 없음"

    # 테이블 데이터 추출
    try:
        sub_board = driver.find_element(By.CSS_SELECTOR, ".sub_board").text.strip()
    except:
        sub_board = "추가 정보 없음"

    logging.info(f"크롤링 완료: {url}")
    return {
        "URL": url,
        "제목": title,
        "카테고리": category,
        "설명": description,
        "추가정보": sub_board
    }

# 전체 URL 크롤링
def scrape_all(URLS):
    driver = get_driver()
    results = []

    for url in URLS:
        result = scrape_page(driver, url)
        results.append(result)

    driver.quit()
    return results
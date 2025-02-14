# 크롤링 데이터 JSON 파일로 저장
import csv
import json
import os

# CSV 형식 저장
def save_to_csv(data, filename="data/seoulnoin_data.csv"):
    """CSV 파일로 저장"""
    os.makedirs("data", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "페이지 제목", "내용"])
        for row in data:
            writer.writerow([row["url"], row["title"], row["content"]])

    print(f"✅ CSV 데이터 저장 완료: {filename}")

# JSON 형식 저장
def save_to_json(data, filename="data/seoulnoin_data.json"):
    """JSON 파일로 저장"""
    os.makedirs("data", exist_ok=True)

    with open(filename, "w", encoding="utf-8-sig") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) 

    print(f"✅ JSON 데이터 저장 완료: {filename}")

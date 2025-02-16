from test_api import test_meal_services
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import logging  # 추가

# 환경 변수 로드
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
   raise ValueError("OPENAI_API_KEY is not set.")

llm = ChatOpenAI(
   openai_api_key = openai_api_key,
   model_name = "gpt-4o-mini",
   temperature = 0.0
)

logging.basicConfig(level=logging.DEBUG) # 디버깅 로그 활성화

def query_chatbot(user_input):
  """사용자의 입력을 분석하고 무료급식소 정보를 제공"""
  
  try:
    logging.debug(f"📥 사용자 입력: {user_input}")

    # OpenAI GPT를 사용해 사용자의 질문을 분석하여 지역명 추출
    prompt = PromptTemplate(
      input_variables = ["user_input"],
      template = (
        "사용자 입력: {user_input}\n\n"
        "아래 항목을 JSON으로 추출(값이 없으면 빈 문자열로):\n"
        "사용자의 질문에서 무료급식소를 찾고 싶은 지역을 추출하세요.\n"
        "지역이 포함되지 않았다면 사용자에게 '지역없음'을 반환하세요.\n\n"
        "예제 입력: '서울 강남구에 무료급식소 어디 있어?'\n"
        "예제 출력: '{\"지역\": \"서울 강남구\"}'"
      )
    )

    # LLM 사용해 지역명 추출
    formatted_prompt = prompt.format(user_input = user_input)
    logging.debug(f"📜 생성된 프롬프트: {formatted_prompt}")

    response = llm.invoke(formatted_prompt)
    logging.debug(f"🤖 LLM 응답: {response}")

    try:
      region_data = eval(response)
      region = region_data("지역", "").strip()
    except json.JSONDecodeError as e:
      logging.error(f"JSON 파싱 오류: {str(e)}")
      region = "지역 없음"

    if "지역 없음" in region:
      return 
      """
      어떤 지역의 무료급식소를 찾고 싶으신가요?
      지역을 말씀해주시면 찾아드리겠습니다😊
      """

    # 해당 지역의 무료급식소 정보 가져오기
    logging.debug(f"🔎 검색할 지역: {region}")
    meal_services = test_meal_services(region)
    logging.debug(f"📊 무료급식소 데이터: {meal_services}")

    if not meal_services or isinstance(meal_services, dict) and "error" in meal_services:
      return "죄송합니다. 해당 지역의 무료급식소 정보를 찾을 수 없습니다."

    response_text = f"🔍 {region} 지역의 무료급식소 정보입니다.\n"
    for service in meal_services:
        response_text += f"🏠 {service['name']} - {service['address']}\n"
    
    return response_text
  
  except Exception as e:
    logging.error(f"🔥 챗봇 내부 오류: {str(e)}", exc_info=True)
    return "죄송합니다. 챗봇에서 오류가 발생했습니다."
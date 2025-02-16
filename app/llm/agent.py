from openai import OpenAI
from app.core.config import settings
from app.services.data_client import PublicDataClient

client = OpenAI(api_key=settings.OPENAI_API_KEY)
data_client = PublicDataClient()

class MealAgent: 
  SYSTEM_PROMPT = """
    당신은 고령층을 위한 무료 급식소 안내 전문가입니다.
    - 65세 이상 대상
    - 주소 설명시 주변 지점 설명
    - 자세한 급식소 안내를 위해 사용자가 이용하고자하는 지역을 추출할 것
    - 이모티콘을 붙여 친근하고, 존댓말을 사용할 것
    """
  
  async def generate_response(self, query: str) -> str:
    # 데이터 수접
    raw_data = data_client.fetch_meal_services()
    context = "\n".join(
      f"{idx+1}. {item['fcltyNm']} ({item['rdnmadr']})"
    for idx, item in enumerate(raw_data)
    )[:3000]

    response = client.chat.completions.create(
      model=settings.LLM_MODEL,
      messages=[
        {"role": "system", "content": self.SYSTEM_PROMPT},
        {"role": "user", "content": f"질문: {query}\n데이터:\n{context}"}
      ],
      temperature=0.3,
      max_tokens=500
    )

    return response.choices[0].message.content
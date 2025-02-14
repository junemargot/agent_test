from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback
from pydantic import BaseModel

from chatbot import query_chatbot

app = FastAPI()

class UserInput(BaseModel):
  user_input: str

@app.get("/")
def root():
    return {"message": "무료급식소 챗봇 API"}

@app.post("/chatbot")
def chatbot_endpoint(data: UserInput):
    """사용자의 입력을 받아 챗봇 응답 반환"""
    try:
      response = query_chatbot(data.user_input)
      return {"response": response}
    except Exception as e:
      error_trace = traceback.format_exc() # 상세 오류 추적
      print(f"🔥 서버 오류 발생:\n{error_trace}")  # 콘솔 출력

      raise HTTPException(status_code=500, detail=f"서버오류발생: {str(e)}")
    
# FastAPI 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

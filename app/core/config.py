from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATA_API_KEY: str
  DATA_DECODING_KEY: str
  OPENAI_API_KEY: str
  APP_TITLE: str = "실버케어 급식서비스"
  APP_DESCRIPTION: str = "고령층 대상 무료 급식소 정보"
  APP_VERSION: str = "1.0"
  LLM_MODEL: str = "gpt-4o-mini"
  
  class Config:
    env_file = ".env",
    extra = "ignore"

settings = Settings()
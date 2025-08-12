from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "telemed"
    ENV: str = "dev"
    SECRET_KEY: str = "please_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "telemed"
    DB_USER: str = "telemed"
    DB_PASSWORD: str = "telemed"

    REDIS_URL: str = "redis://localhost:6379/0"

    STRIPE_SECRET_KEY: str = "sk_test_change_me"
    STRIPE_WEBHOOK_SECRET: str = "whsec_change_me"

    SENDGRID_API_KEY: str = "SG.change_me"
    EMAIL_FROM: str = "no-reply@demo.local"

    TWILIO_ACCOUNT_SID: str = "AC_change_me"
    TWILIO_AUTH_TOKEN: str = "change_me"
    TWILIO_WHATSAPP_FROM: str = "whatsapp:+14155238886"

    FILE_STORAGE_PATH: str = "/data"
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = "backend/.env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

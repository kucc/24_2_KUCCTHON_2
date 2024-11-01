import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    # 환경 설정
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # 공통 설정
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRATION_TIME_MINUTES: int = int(os.getenv("JWT_ACCESS_EXPIRATION_TIME_MINUTES", 30))
    JWT_REFRESH_EXPIRATION_TIME_MINUTES: int = int(os.getenv("JWT_REFRESH_EXPIRATION_TIME_MINUTES", 60))

    APP_TITLE: str = "Library Management System"
    APP_DESCRIPTION: str = "API for managing library resources"
    APP_VERSION: str = "0.1.0"

    FIREBASE_SERVICE_ACCOUNT_KEY: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "firebase-service-account-key.json")
    FIREBASE_WEB_API_KEY: str = os.getenv("FIREBASE_WEB_API_KEY", "firebase-web-api-key")

    # Experiment/Development 데이터베이스 설정
    EXP_DB_HOST: str = os.getenv("EXP_DB_HOST", "localhost")
    EXP_DB_PORT: int = int(os.getenv("EXP_DB_PORT", 3306))
    EXP_DB_NAME: str = os.getenv("EXP_DB_NAME", "exp_library_db")
    EXP_DB_USER: str = os.getenv("EXP_DB_USER", "exp_user")
    EXP_DB_PASSWORD: str = os.getenv("EXP_DB_PASSWORD", "exp_password")

    @property
    def DATABASE_URL(self):
        if self.ENVIRONMENT == "development":
            return f"mysql+pymysql://{self.EXP_DB_USER}:{self.EXP_DB_PASSWORD}@{self.EXP_DB_HOST}:{self.EXP_DB_PORT}/{self.EXP_DB_NAME}"


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Parking-System"
    DATABASE_URL: str = "postgresql://parking_user:parking_password@localhost:5432/parking_db"
    
    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()
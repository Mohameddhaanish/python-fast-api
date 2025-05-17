import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM:str=os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    GOOGLE_APP_KEY:str=os.getenv("GOOGLE_APP_KEY")
    CRYPTO_JS_SECRET:str=os.getenv("CRYPTO_JS_SECRET")
    
settings = Settings()

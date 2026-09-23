import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("DATABASE_HOST"),
    "port": os.getenv("DATABASE_PORT"),
    "dbname": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
}

TELEGRAM_CONFIG = {
    "api_id": os.getenv("TELEGRAM_API_ID"),
    "api_hash": os.getenv("TELEGRAM_API_HASH"),
    "phone": os.getenv("TELEGRAM_PHONE"),
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "bot_username": os.getenv("TELEGRAM_BOT_USERNAME"),
}

# Secret key for signing auth tokens
SECRET_KEY = os.getenv("SECRET_KEY", "pixelvault-dev-secret-change-in-prod")

# Configuration for CompreFace service
COMPREFACE_CONFIG = {
    "host": os.getenv("COMPREFACE_HOST"),
    "api_key": os.getenv("COMPREFACE_API_KEY"),
}

# Configuration for Ollama (LLaVA) AI service
OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "model": os.getenv("OLLAMA_MODEL"),
}


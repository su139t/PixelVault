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
}


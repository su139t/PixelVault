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

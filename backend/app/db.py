import psycopg

from app.config.settings import DATABASE_CONFIG


def get_db_connection():
    return psycopg.connect(**DATABASE_CONFIG)

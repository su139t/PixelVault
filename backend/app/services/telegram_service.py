from pathlib import Path

from telethon import TelegramClient

from app.config.settings import TELEGRAM_CONFIG


BASE_DIR = Path(__file__).resolve().parents[2]
SESSION_PATH = BASE_DIR / "pixelvault.session"


def get_client():
    api_id = TELEGRAM_CONFIG.get("api_id")
    api_hash = TELEGRAM_CONFIG.get("api_hash")

    if not api_id or not api_hash:
        raise ValueError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env"
        )

    return TelegramClient(str(SESSION_PATH), int(api_id), api_hash)


async def login():
    client = get_client()
    await client.start(phone=TELEGRAM_CONFIG.get("phone"))
    return client

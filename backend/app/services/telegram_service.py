import asyncio
import hashlib
import re
import threading
import time
from io import BytesIO
from pathlib import Path

from telethon import TelegramClient, errors

from app.config.settings import TELEGRAM_CONFIG


BASE_DIR = Path(__file__).resolve().parents[2]
SESSION_PATH = BASE_DIR / "pixelvault.session"
USER_SESSIONS_DIR = BASE_DIR / ".telegram_sessions"
PENDING_LOGIN_TTL = 600
PHONE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")

_pending_logins = {}
_pending_lock = threading.Lock()
_authorized_clients = {}

# Global client instance
_client = None


def _get_api_credentials():
    api_id = TELEGRAM_CONFIG.get("api_id")
    api_hash = TELEGRAM_CONFIG.get("api_hash")

    if not api_id or not api_hash:
        raise ValueError("TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env")

    try:
        return int(api_id), api_hash
    except (TypeError, ValueError) as exc:
        raise ValueError("TELEGRAM_API_ID must be a valid integer") from exc


def _normalize_phone(phone_number):
    normalized = re.sub(r"[\s().-]", "", str(phone_number or ""))
    if not PHONE_PATTERN.fullmatch(normalized):
        raise ValueError("Enter a valid phone number with country code")
    return normalized


def _session_path(phone_number):
    USER_SESSIONS_DIR.mkdir(mode=0o700, exist_ok=True)
    digest = hashlib.sha256(phone_number.encode("utf-8")).hexdigest()
    return USER_SESSIONS_DIR / digest


def _new_user_client(phone_number):
    api_id, api_hash = _get_api_credentials()
    return TelegramClient(str(_session_path(phone_number)), api_id, api_hash)


async def _get_client_for_user(user_id):
    """Return the authorized Telethon session belonging to a PixelVault user."""
    from app.repositories.users_repository import get_user_by_id

    user = get_user_by_id(user_id)
    if not user or not user[1]:
        raise ValueError("Telegram account is not linked to this PixelVault user")

    telegram_user_id = int(user[1])
    # Media routes use short-lived asyncio loops, so clients cannot be reused
    # safely between requests.
    cached = _authorized_clients.pop(telegram_user_id, None)
    if cached and cached.is_connected():
        await cached.disconnect()

    if not USER_SESSIONS_DIR.exists():
        raise ValueError("Telegram session not found. Please sign in again")

    api_id, api_hash = _get_api_credentials()
    for session_file in USER_SESSIONS_DIR.iterdir():
        if not session_file.is_file() or session_file.name.endswith(".journal"):
            continue
        client = TelegramClient(str(session_file), api_id, api_hash)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                await client.disconnect()
                continue
            telegram_user = await client.get_me()
            if telegram_user and int(telegram_user.id) == telegram_user_id:
                return client
            await client.disconnect()
        except Exception:
            if client.is_connected():
                await client.disconnect()

    raise ValueError("Telegram session not found. Please sign in again")


def _prune_pending_logins():
    now = time.time()
    expired = [
        phone for phone, data in _pending_logins.items()
        if now - data["created_at"] > PENDING_LOGIN_TTL
    ]
    for phone in expired:
        _pending_logins.pop(phone, None)


def _telegram_error_message(error):
    if isinstance(error, errors.PhoneNumberInvalidError):
        return "Telegram rejected this phone number"
    if isinstance(error, errors.PhoneCodeInvalidError):
        return "The Telegram code is invalid"
    if isinstance(error, errors.PhoneCodeEmptyError):
        return "Enter the Telegram verification code"
    if isinstance(error, errors.PhoneCodeHashEmptyError):
        return "The verification request is invalid. Request a new code"
    if isinstance(error, errors.PhoneCodeExpiredError):
        return "The Telegram code has expired. Request a new code"
    if isinstance(error, errors.AuthRestartError):
        return "Telegram restarted this login. Request a new code"
    if isinstance(error, errors.FloodWaitError):
        return f"Too many attempts. Try again in {error.seconds} seconds"
    if isinstance(error, (errors.ApiIdInvalidError, errors.AuthKeyError)):
        return "Telegram API credentials are invalid"
    if isinstance(error, (errors.RPCError, ConnectionError, OSError)):
        return "Could not connect to Telegram. Please try again"
    return "Telegram authentication failed"


async def _send_code(phone_number, force_code=False):
    client = _new_user_client(phone_number)
    try:
        await client.connect()
        if await client.is_user_authorized():
            if force_code:
                await client.log_out()
                await client.disconnect()
                session_file = _session_path(phone_number)
                session_file.unlink(missing_ok=True)
                Path(f"{session_file}-journal").unlink(missing_ok=True)
                client = _new_user_client(phone_number)
                await client.connect()
            else:
                return {"already_authenticated": True, "user": await client.get_me()}

        sent_code = await client.send_code_request(phone_number)
        with _pending_lock:
            _prune_pending_logins()
            _pending_logins[phone_number] = {
                "phone_code_hash": sent_code.phone_code_hash,
                "created_at": time.time(),
            }
        return {"already_authenticated": False}
    finally:
        await client.disconnect()


def send_code(phone_number, force_code=False):
    normalized = _normalize_phone(phone_number)
    try:
        return asyncio.run(_send_code(normalized, force_code=force_code))
    except ValueError:
        raise
    except Exception as error:
        raise ValueError(_telegram_error_message(error)) from error


async def _verify_code(phone_number, code):
    with _pending_lock:
        _prune_pending_logins()
        login = _pending_logins.get(phone_number)
    if not login:
        raise ValueError("Your code request has expired. Request a new code")

    client = _new_user_client(phone_number)
    try:
        await client.connect()
        try:
            user = await client.sign_in(
                phone=phone_number,
                code=str(code).strip(),
                phone_code_hash=login["phone_code_hash"],
            )
        except errors.SessionPasswordNeededError:
            return {"password_required": True}
        with _pending_lock:
            _pending_logins.pop(phone_number, None)
        return {"password_required": False, "user": user or await client.get_me()}
    finally:
        await client.disconnect()


def verify_code(phone_number, code):
    normalized = _normalize_phone(phone_number)
    if not str(code or "").strip():
        raise ValueError("Telegram code is required")
    try:
        return asyncio.run(_verify_code(normalized, code))
    except ValueError:
        raise
    except Exception as error:
        raise ValueError(_telegram_error_message(error)) from error


async def _verify_2fa(phone_number, password):
    with _pending_lock:
        _prune_pending_logins()
        if phone_number not in _pending_logins:
            raise ValueError("Your Telegram login request has expired. Request a new code")

    client = _new_user_client(phone_number)
    try:
        await client.connect()
        user = await client.sign_in(phone=phone_number, password=password)
        with _pending_lock:
            _pending_logins.pop(phone_number, None)
        return user or await client.get_me()
    finally:
        await client.disconnect()


def verify_2fa(phone_number, password):
    normalized = _normalize_phone(phone_number)
    if not password:
        raise ValueError("Telegram 2FA password is required")
    try:
        return asyncio.run(_verify_2fa(normalized, password))
    except ValueError:
        raise
    except Exception as error:
        if isinstance(error, errors.PasswordHashInvalidError):
            raise ValueError("The Telegram 2FA password is incorrect") from error
        raise ValueError(_telegram_error_message(error)) from error


def get_client():
    global _client
    if _client is not None:
        return _client

    api_id = TELEGRAM_CONFIG.get("api_id")
    api_hash = TELEGRAM_CONFIG.get("api_hash")

    if not api_id or not api_hash:
        raise ValueError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env"
        )

    _client = TelegramClient(str(SESSION_PATH), int(api_id), api_hash)
    return _client


async def ensure_connected():
    client = get_client()
    if not client.is_connected():
        await client.connect()
        if not await client.is_user_authorized():
            # In a real app we'd need to handle auth here, but since we have a 
            # script for login, we assume the session is valid.
            await client.start(phone=TELEGRAM_CONFIG.get("phone"))
    return client


async def upload_to_saved_messages_for_user(user_id, file_or_path, caption=None):
    """Upload a file to Saved Messages. file_or_path can be string path or BytesIO."""
    client = await _get_client_for_user(user_id)
    try:
        entity = await client.get_entity("me")

        if isinstance(file_or_path, BytesIO) and not hasattr(file_or_path, "name"):
            file_or_path.name = "image.jpg"

        msg = await client.send_file(entity, file_or_path, caption=caption)
        return {
            "telegram_chat_id": entity.id,
            "telegram_message_id": msg.id
        }
    finally:
        await client.disconnect()


async def download_media_for_user(user_id, chat_id, message_id):
    client = await _get_client_for_user(user_id)
    try:
        message = await client.get_messages(chat_id, ids=message_id)
        if not message or not message.media:
            raise ValueError("Message or media not found")

        output = BytesIO()
        await client.download_media(message, output)
        output.seek(0)
        return output
    finally:
        await client.disconnect()


async def delete_message_for_user(user_id, chat_id, message_id):
    client = await _get_client_for_user(user_id)
    try:
        await client.delete_messages(chat_id, [message_id])
        return True
    finally:
        await client.disconnect()


async def _revoke_user_session(user_id):
    """Disconnect and remove the session for an explicit PixelVault logout."""
    from app.repositories.users_repository import get_user_by_id

    user = get_user_by_id(user_id)
    if not user or not user[1]:
        return

    telegram_user_id = int(user[1])
    client = _authorized_clients.pop(telegram_user_id, None)
    if client and client.is_connected():
        try:
            await client.log_out()
        finally:
            await client.disconnect()

    with _pending_lock:
        _pending_logins.clear()

    global _client
    if _client and _client.is_connected():
        try:
            await _client.log_out()
        finally:
            await _client.disconnect()
    _client = None
    SESSION_PATH.unlink(missing_ok=True)
    Path(f"{SESSION_PATH}-journal").unlink(missing_ok=True)

    if not USER_SESSIONS_DIR.exists():
        return

    api_id, api_hash = _get_api_credentials()
    for session_file in USER_SESSIONS_DIR.iterdir():
        if not session_file.is_file() or session_file.name.endswith(".journal"):
            continue
        candidate = TelegramClient(str(session_file), api_id, api_hash)
        try:
            await candidate.connect()
            telegram_user = await candidate.get_me() if await candidate.is_user_authorized() else None
            if telegram_user and int(telegram_user.id) == telegram_user_id:
                await candidate.log_out()
                session_file.unlink(missing_ok=True)
                Path(f"{session_file}-journal").unlink(missing_ok=True)
            await candidate.disconnect()
        except Exception:
            if candidate.is_connected():
                await candidate.disconnect()


def revoke_user_session(user_id):
    try:
        asyncio.run(_revoke_user_session(user_id))
    except ValueError:
        raise
    except Exception as error:
        raise ValueError("Could not sign out from Telegram") from error


async def download_media(chat_id, message_id):
    """Download media from Telegram into memory (BytesIO)."""
    client = await ensure_connected()
    
    # Get the specific message
    message = await client.get_messages(chat_id, ids=message_id)
    if not message or not message.media:
        raise ValueError("Message or media not found")
        
    output = BytesIO()
    await client.download_media(message, output)
    output.seek(0)
    
    return output


async def delete_message(chat_id, message_id):
    """Delete a message from Telegram."""
    client = await ensure_connected()
    await client.delete_messages(chat_id, [message_id])
    return True


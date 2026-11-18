import hashlib
import hmac
import time

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.config.settings import TELEGRAM_CONFIG, SECRET_KEY
from app.repositories.users_repository import (
    get_user_by_telegram_id,
    upsert_user,
)


# Token serializer (24-hour expiry)
TOKEN_MAX_AGE = 86400
_serializer = URLSafeTimedSerializer(SECRET_KEY)


def validate_telegram_login(data):
    """
    Validate the Telegram Login Widget data hash.
    See: https://core.telegram.org/widgets/login#checking-authorization
    """
    bot_token = TELEGRAM_CONFIG.get("bot_token")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured")

    # Extract and remove hash from data
    received_hash = data.get("hash")
    if not received_hash:
        raise ValueError("Missing hash in Telegram login data")

    # Check auth_date is not too old (allow 1 day)
    auth_date = data.get("auth_date")
    if auth_date:
        if time.time() - int(auth_date) > 86400:
            raise ValueError("Telegram login data is expired")

    # Build the check string: sorted key=value pairs (excluding hash)
    check_data = {k: v for k, v in data.items() if k != "hash"}
    check_string = "\n".join(
        f"{k}={check_data[k]}" for k in sorted(check_data.keys())
    )

    # secret_key = SHA256(bot_token)
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()

    # HMAC-SHA256(check_string, secret_key)
    computed_hash = hmac.new(
        secret_key,
        check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise ValueError("Invalid Telegram login hash")

    return True


def find_or_create_user(telegram_data):
    """
    Find existing user by telegram_user_id or create a new one.
    Returns user tuple.
    """
    telegram_user_id = telegram_data.get("id")
    if not telegram_user_id:
        raise ValueError("Missing Telegram user id")

    first_name = telegram_data.get("first_name", "")
    last_name = telegram_data.get("last_name", "")
    name = f"{first_name} {last_name}".strip() or "Telegram User"
    username = telegram_data.get("username")
    photo_url = telegram_data.get("photo_url")

    # Try to find existing user
    user = get_user_by_telegram_id(int(telegram_user_id))

    if user:
        return user

    # Create new user via upsert
    user = upsert_user(
        telegram_user_id=int(telegram_user_id),
        name=name,
        username=username,
    )

    return user


def generate_token(user):
    """Generate a signed token containing the user_id."""
    user_id = user[0]
    return _serializer.dumps({"user_id": user_id})


def verify_token(token):
    """Verify and decode a token. Returns payload dict or raises."""
    try:
        payload = _serializer.loads(token, max_age=TOKEN_MAX_AGE)
        return payload
    except SignatureExpired:
        raise ValueError("Token has expired")
    except BadSignature:
        raise ValueError("Invalid token")

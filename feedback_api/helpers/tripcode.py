import hashlib
import hmac
from django.conf import settings

DEFAULT_SEPARATOR = "!"

def make_tripcode(username: str, secret: str, separator: str = DEFAULT_SEPARATOR) -> str:
    salt = settings.TRIPCODE_SALT
    raw = f"{username}:{secret}:{salt}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()[:16]
    return f"{username}{separator}{digest}"

def verify_tripcode(tripcode: str, username: str, secret: str, separator: str = DEFAULT_SEPARATOR) -> bool:
    expected = make_tripcode(username, secret, separator)
    return hmac.compare_digest(tripcode, expected)

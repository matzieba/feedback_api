import hashlib
import hmac
import settings

DEFAULT_SEPARATOR = "!"

def make_tripcode(username, secret, separator=DEFAULT_SEPARATOR):
    salt = settings.TRIPCODE_SALT
    raw = f"{username}:{secret}:{salt}".encode("utf-8")
    digest = hmac.new(salt.encode("utf-8"), raw, hashlib.sha256).hexdigest()[:16]
    tripcode = f"{username}{separator}{digest}"
    return tripcode

def verify_tripcode(tripcode, username, secret, separator=DEFAULT_SEPARATOR):
    expected_tripcode = make_tripcode(username, secret, separator)
    return hmac.compare_digest(tripcode, expected_tripcode)
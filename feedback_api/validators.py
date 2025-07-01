from rest_framework import serializers

from feedback_api.constants import FORBIDDEN_USERNAME_CHARS


def validate_secret(secret: str):
    if len(secret) < 8:
        raise serializers.ValidationError("Secret must be at least 8 characters long.")
    if secret.isspace():
        raise serializers.ValidationError("Secret cannot be only whitespace.")
    if secret.isdigit() or secret.isalpha():
        raise serializers.ValidationError("Secret must contain both letters and digits or symbols.")
    return secret

def validate_username(username: str):
    if any(char in username for char in FORBIDDEN_USERNAME_CHARS):
        raise serializers.ValidationError(
            f"Username must not contain any of the following characters: {FORBIDDEN_USERNAME_CHARS}"
        )
    if not username.isprintable() or username.strip() == "":
        raise serializers.ValidationError("Username contains invalid or control characters.")
    if len(username) > 32:
        raise serializers.ValidationError("Username too long (max 32 characters).")
    return username
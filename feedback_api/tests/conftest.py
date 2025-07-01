import pytest
from datetime import timedelta
from django.utils import timezone
from model_bakery import baker


@pytest.fixture
def inbox():
    return baker.make(
        "feedback_api.Inbox",
        signature="testowner!12345678abcdef",
        expiration_date=timezone.now() + timedelta(days=1),
        allow_anonymous=True,
    )


@pytest.fixture
def expired_inbox():
    return baker.make(
        "feedback_api.Inbox",
        signature="testowner!12345678abcdef",
        expiration_date=timezone.now() - timedelta(days=1),
        allow_anonymous=True,
    )


@pytest.fixture
def message(inbox):
    return baker.make(
        "feedback_api.Message", inbox=inbox, body="hi", signature="anon!aaaaa"
    )

import pytest
from datetime import timedelta
from django.utils import timezone
from model_bakery import baker

from feedback_api.helpers.tripcode import make_tripcode


@pytest.fixture
def inbox_data():
    return {"owner": "testowner", "secret": "12345678abcdef"}


@pytest.fixture
def inbox(inbox_data):
    return baker.make(
        "feedback_api.Inbox",
        signature=make_tripcode(inbox_data["owner"], inbox_data["secret"]),
        expiration_date=timezone.now() + timedelta(days=1),
        allow_anonymous=True,
    )


@pytest.fixture
def expired_inbox(inbox_data):
    return baker.make(
        "feedback_api.Inbox",
        signature=make_tripcode(inbox_data["owner"], inbox_data["secret"]),
        expiration_date=timezone.now() - timedelta(days=1),
        allow_anonymous=True,
    )


@pytest.fixture
def message(inbox):
    return baker.make(
        "feedback_api.Message", inbox=inbox, body="hi", signature="anon!aaaaa"
    )


@pytest.fixture
def message_factory(inbox):
    def factory(**kwargs):
        return baker.make("feedback_api.Message", **kwargs)

    return factory

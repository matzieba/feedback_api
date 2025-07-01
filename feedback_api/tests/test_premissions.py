import pytest
from rest_framework.test import APIClient
from feedback_api.models import Inbox
from feedback_api.helpers import make_tripcode


@pytest.mark.django_db
def test_is_inbox_owner_permission_passes(settings):
    username = "permsowner"
    secret = "sekret"
    tripcode = make_tripcode(username, secret)
    inbox = Inbox.objects.create(
        topic="t",
        signature=tripcode,
        expiration_date="2100-01-01",
        allow_anonymous=True,
    )
    client = APIClient()
    response = client.post(
        f"/inboxes/{inbox.pk}/edit-topic/",
        {"username": username, "secret": secret, "topic": "new topic"},
        format="json",
    )
    assert response.status_code == 200
    inbox.refresh_from_db()
    assert inbox.topic == "new topic"


@pytest.mark.django_db
def test_is_inbox_owner_permission_fails(settings):
    username = "rightuser"
    secret = "pass1"
    tripcode = make_tripcode(username, secret)
    inbox = Inbox.objects.create(
        topic="t",
        signature=tripcode,
        expiration_date="2100-01-01",
        allow_anonymous=True,
    )
    client = APIClient()
    response = client.post(
        f"/inboxes/{inbox.pk}/edit-topic/",
        {"username": "wronguser", "secret": "bleh", "topic": "new topic"},
        format="json",
    )
    assert response.status_code == 403

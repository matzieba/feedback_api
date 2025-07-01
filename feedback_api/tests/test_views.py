# tests/test_views.py

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from feedback_api.helpers import make_tripcode
from feedback_api.models import Inbox


@pytest.mark.django_db
def test_inbox_edit_topic_api_success(settings):
    username, secret = "apiuser", "keepit"
    tripcode = make_tripcode(username, secret)
    inbox = Inbox.objects.create(
        topic="orig",
        signature=tripcode,
        expiration_date="2100-01-01",
        allow_anonymous=True,
    )
    client = APIClient()
    url = f"/inboxes/{inbox.pk}/edit-topic/"
    resp = client.post(url, {"topic": "new", "username": username, "secret": secret})
    assert resp.status_code == 200
    inbox.refresh_from_db()
    assert inbox.topic == "new"


@pytest.mark.django_db
def test_inbox_edit_topic_api_forbidden(settings):
    inbox = baker.make("feedback_api.Inbox", expiration_date="2100-01-01")
    client = APIClient()
    url = f"/inboxes/{inbox.pk}/edit-topic/"
    resp = client.post(url, {"topic": "new", "username": "x", "secret": "y"})
    assert resp.status_code == 403


@pytest.mark.django_db
def test_reply_post_and_reply_read(settings):
    username, secret = "apiowner", "heavysecret"
    tripcode = make_tripcode(username, secret)
    inbox = Inbox.objects.create(
        topic="Hello feedback",
        signature=tripcode,
        expiration_date="2100-01-01",
        allow_anonymous=True,
    )
    client = APIClient()
    # Anyone can post message
    reply_url = f"/inboxes/{inbox.pk}/messages/"
    resp = client.post(reply_url, {"body": "feedback about you!"})
    assert resp.status_code == 201

    # Only owner can see replies
    api_url = f"/inboxes/{inbox.pk}/replies/"
    resp = client.post(api_url, {"username": username, "secret": secret})
    assert resp.status_code == 200
    assert resp.data[0]["body"] == "feedback about you!"

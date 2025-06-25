# tests/test_inbox_owner_api.py
import pytest
from django.urls import reverse
from django.utils import timezone

from feedback_api.helpers import make_tripcode
from feedback_api.models.inbox import Inbox
from feedback_api.models.message import Message

@pytest.mark.django_db
def test_owner_can_view_replies(client):
    code = make_tripcode("anna", "wow")
    inbox = Inbox.objects.create(
        topic="Ask me",
        signature=code,
        expiration_date=timezone.now() + timezone.timedelta(days=1),
        allow_anonymous=True,
    )
    Message.objects.create(inbox=inbox, body="yo", signature="a!123")
    Message.objects.create(inbox=inbox, body="hi there")
    url = reverse("inbox-replies", kwargs={"inbox_pk": inbox.id})
    # Wrong/no credentials
    r = client.post(url, {"username": "anna", "secret": "bad"}, content_type="application/json")
    assert r.status_code == 403
    # Missing creds
    r2 = client.post(url, {}, content_type="application/json")
    assert r2.status_code == 400
    # Good credentials
    r3 = client.post(url, {"username": "anna", "secret": "wow"}, content_type="application/json")
    assert r3.status_code == 200
    replies = r3.json()
    assert len(replies) == 2
    assert replies[0]["body"] == "yo"
    assert replies[1]["body"] == "hi there"

@pytest.mark.django_db
def test_edit_topic_requires_owner_and_zero_replies(client):
    code = make_tripcode("tom", "way2go")
    inbox = Inbox.objects.create(
        topic="Original",
        signature=code,
        expiration_date=timezone.now() + timezone.timedelta(days=1),
        allow_anonymous=True,
    )
    url = reverse("inbox-edit-topic", kwargs={"inbox_pk": inbox.id})
    # Wrong credentials
    r1 = client.post(url, {"topic": "New", "username": "tom", "secret": "nope"}, content_type="application/json")
    assert r1.status_code == 400
    # Works if 0 replies
    r2 = client.post(url, {"topic": "NewQ", "username": "tom", "secret": "way2go"}, content_type="application/json")
    assert r2.status_code == 200
    assert r2.json()["topic"] == "NewQ"
    # Add reply
    Message.objects.create(inbox=inbox, body="hey")
    # Now edit _should_ fail
    r3 = client.post(url, {"topic": "Another", "username": "tom", "secret": "way2go"}, content_type="application/json")
    assert r3.status_code == 400
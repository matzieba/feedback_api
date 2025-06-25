# tests/test_message_api.py

import pytest
from django.urls import reverse
from django.utils import timezone

from feedback_api.helpers import make_tripcode
from feedback_api.models.inbox import Inbox


@pytest.mark.django_db
def test_message_create_anonymous_and_signed(client):
    tripcode = make_tripcode("bob", "pw4")
    inbox = Inbox.objects.create(
        topic="Feedback",
        signature=tripcode,
        expiration_date=timezone.now() + timezone.timedelta(days=1),
        allow_anonymous=True,
    )

    # Anonymous reply (allowed)
    url = reverse("message-create", kwargs={"inbox_pk": inbox.id})
    r1 = client.post(url, {"body": "Great job!"}, content_type="application/json")
    assert r1.status_code == 201

    # Signed reply (allowed)
    r2 = client.post(url, {"body": "Signed reply", "signature": "bob!fakehash"}, content_type="application/json")
    assert r2.status_code == 201

    # For non-anon inbox, signature required
    inbox2 = Inbox.objects.create(
        topic="Non-anon",
        signature=tripcode,
        expiration_date=timezone.now() + timezone.timedelta(days=1),
        allow_anonymous=False,
    )
    url2 = reverse("message-create", kwargs={"inbox_pk": inbox2.id})
    # No signature: should fail
    r3 = client.post(url2, {"body": "No sig"}, content_type="application/json")
    assert r3.status_code == 400

    # With signature: OK
    r4 = client.post(url2, {"body": "With sig", "signature": "bob!fakehash"}, content_type="application/json")
    assert r4.status_code == 201

@pytest.mark.django_db
def test_message_not_allowed_when_expired(client):
    tripcode = make_tripcode("bob", "pw4")
    inbox = Inbox.objects.create(
        topic="Expired",
        signature=tripcode,
        expiration_date=timezone.now() - timezone.timedelta(hours=1),
        allow_anonymous=True,
    )
    url = reverse("message-create", kwargs={"inbox_pk": inbox.id})
    r = client.post(url, {"body": "Late reply"}, content_type="application/json")
    assert r.status_code == 400
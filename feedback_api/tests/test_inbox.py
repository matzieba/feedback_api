import pytest
from django.utils import timezone
from rest_framework.reverse import reverse

from feedback_api.helpers import make_tripcode
from feedback_api.models import Inbox


def test_inbox_create(client, db):
    resp = client.post(
        '/api/inboxes/',
        {
            "topic": "Feedback?",
            "expiration_date": "2024-08-01T00:00:00Z",
            "allow_anonymous": True,
            "username": "me",
            "secret": "mysecret"
        },
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["topic"] == "Feedback?"

@pytest.mark.django_db
def test_inbox_creation_and_detail(client):
    # Test Inbox creation via POST
    url = reverse("inbox-list")  # POST for create on ViewSet router
    response = client.post(url, {
        "topic": "What do you like about me?",
        "expiration_date": (timezone.now() + timezone.timedelta(days=10)).isoformat(),
        "allow_anonymous": True,
        "username": "alice",
        "secret": "supersecret"
    }, content_type="application/json")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    # Grab the UUID for detail API
    inbox_id = data["id"]

    # Test detail endpoint via GET
    detail_url = reverse("inbox-detail", kwargs={"pk": inbox_id})
    detail_resp = client.get(detail_url)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["id"] == inbox_id
    assert detail["topic"] == "What do you like about me?"
    assert detail["allow_anonymous"] is True
    # If you're exposing owner_name:
    assert detail["owner_name"] == "alice"

@pytest.mark.django_db
def test_inbox_detail_not_found(client):
    # Random UUID that does not exist
    import uuid
    url = reverse("inbox-detail", kwargs={"pk": str(uuid.uuid4())})
    r = client.get(url)
    assert r.status_code == 404

# Optional: Only if you expose list endpoint for staff/dev/admin
@pytest.mark.django_db
def test_inbox_list_optional(client):
    # Create two inboxes directly in DB
    Inbox.objects.create(
        topic="a", signature=make_tripcode("x","1"),
        expiration_date=timezone.now()+timezone.timedelta(days=1)
    )
    Inbox.objects.create(
        topic="b", signature=make_tripcode("y","2"),
        expiration_date=timezone.now()+timezone.timedelta(days=1)
    )
    url = reverse("inbox-list")
    r = client.get(url)
    assert r.status_code == 200
    data = r.json()
    assert type(data) is list
    assert any(d['topic'] == "a" for d in data)
    assert any(d['topic'] == "b" for d in data)


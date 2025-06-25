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
import pytest
from feedback_api.helpers import make_tripcode


@pytest.mark.django_db
def test_is_expired_logic(inbox, expired_inbox):
    assert not inbox.is_expired
    assert expired_inbox.is_expired


@pytest.mark.django_db
def test_owner_matches_works(inbox, settings):
    username = "username1"
    secret = "supersecret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()

    assert inbox.owner_matches(username, secret)
    assert not inbox.owner_matches("wronguser", secret)
    assert not inbox.owner_matches(username, "wrongsecret")


@pytest.mark.django_db
def test_change_topic_only_owner_and_no_replies(inbox, settings):
    username = "topicboss"
    secret = "sekret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()
    inbox.messages.all().delete()
    inbox.change_topic("New topic here", username=username, secret=secret)

    assert inbox.topic == "New topic here"


@pytest.mark.django_db
def test_change_topic_fails_after_replies(inbox, message, settings):
    username = "topicboss"
    secret = "sekret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()

    with pytest.raises(ValueError):
        inbox.change_topic("nope", username=username, secret=secret)


@pytest.mark.django_db
def test_change_topic_fails_not_owner(inbox, settings):
    inbox.signature = make_tripcode("trueowner", "sekret")
    inbox.save()

    with pytest.raises(PermissionError):
        inbox.change_topic("blabla", username="hacker", secret="sekret")

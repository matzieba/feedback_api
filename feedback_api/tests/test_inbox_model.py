import pytest
from feedback_api.helpers import make_tripcode
from feedback_api.services.inbox import InboxService

@pytest.mark.django_db
def test_is_expired_logic(inbox, expired_inbox):
    assert not InboxService.is_expired(inbox)
    assert InboxService.is_expired(expired_inbox)


@pytest.mark.django_db
def test_owner_matches_works(inbox, settings):
    username = "username1"
    secret = "supersecret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()

    assert InboxService.owner_matches(inbox, username, secret)
    assert not InboxService.owner_matches(inbox, "wronguser", secret)
    assert not InboxService.owner_matches(inbox, username, "wrongsecret")


@pytest.mark.django_db
def test_change_topic_only_owner_and_no_replies(inbox, settings):
    username = "topicboss"
    secret = "sekret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()
    inbox.messages.all().delete()

    InboxService.change_topic(inbox, "New topic here", username=username, secret=secret)

    assert inbox.topic == "New topic here"


@pytest.mark.django_db
def test_change_topic_fails_after_replies(inbox, message, settings):
    username = "topicboss"
    secret = "sekret"
    inbox.signature = make_tripcode(username, secret)
    inbox.save()

    with pytest.raises(PermissionError):
        InboxService.change_topic(inbox, "nope", username=username, secret=secret)


@pytest.mark.django_db
def test_change_topic_fails_not_owner(inbox, settings):
    inbox.signature = make_tripcode("trueowner", "sekret")
    inbox.save()

    with pytest.raises(PermissionError):
        InboxService.change_topic(inbox, "blabla", username="hacker", secret="sekret")
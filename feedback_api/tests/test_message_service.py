
import pytest

from feedback_api.services.message import add_message_to_inbox


@pytest.mark.django_db
def test_add_message_to_inbox_success(inbox):
    msg = add_message_to_inbox(inbox, "feedback", None)
    assert msg.body == "feedback"
    assert msg.signature is None
    assert msg.inbox == inbox


@pytest.mark.django_db
def test_add_message_to_inbox_requires_signature(inbox):
    inbox.allow_anonymous = False
    inbox.save()
    with pytest.raises(ValueError):
        add_message_to_inbox(inbox, "cannot post", None)


@pytest.mark.django_db
def test_add_message_to_expired_inbox(expired_inbox):
    with pytest.raises(ValueError):
        add_message_to_inbox(expired_inbox, "nope", None)

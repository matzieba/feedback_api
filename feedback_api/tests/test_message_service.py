
import pytest
from django.core.exceptions import ValidationError
from django.db import DataError

from feedback_api.models.message import Message
from feedback_api.services.message import MessageService


@pytest.mark.django_db
def test_add_message_to_inbox_success(inbox):
    msg = MessageService.add_message_to_inbox(inbox, "feedback", None)
    assert msg.body == "feedback"
    assert msg.signature is None
    assert msg.inbox == inbox


@pytest.mark.django_db
def test_add_message_to_inbox_requires_signature(inbox):
    inbox.allow_anonymous = False
    inbox.save()
    with pytest.raises(ValueError):
        MessageService.add_message_to_inbox(inbox, "cannot post", None)


@pytest.mark.django_db
def test_add_message_to_expired_inbox(expired_inbox):
    with pytest.raises(ValueError):
        MessageService.add_message_to_inbox(expired_inbox, "nope", None)

@pytest.mark.django_db
def test_add_message_long_body_and_signature(inbox):
    long_body = "a" * 1600
    long_signature = "b" * 260
    with pytest.raises(DataError):
        MessageService.add_message_to_inbox(inbox, long_body, long_signature)


@pytest.mark.django_db
def test_add_message_unicode_support(inbox):
    unicode_body = "こんにちは世界"
    unicode_signature = "😊"
    msg = MessageService.add_message_to_inbox(inbox, unicode_body, unicode_signature)
    assert msg.body == unicode_body
    assert msg.signature == unicode_signature


@pytest.mark.django_db
def test_get_messages_for_inbox(inbox, message_factory):
    message_factory(inbox=inbox)
    message_factory(inbox=inbox)
    messages = MessageService.get_messages_for_inbox(inbox)
    assert messages.count() == 2


@pytest.mark.django_db
def test_get_message_by_id(message):
    msg = MessageService.get_message_by_id(message.id)
    assert msg == message


@pytest.mark.django_db
def test_get_message_by_id_not_found(message):
    with pytest.raises(Message.DoesNotExist):
        MessageService.get_message_by_id(message.id + 1)


@pytest.mark.django_db
def test_delete_message_success(message, inbox_data):
    MessageService.delete_message(message, inbox_data["owner"], inbox_data["secret"])
    assert MessageService.get_messages_for_inbox(message.inbox).count() == 0


@pytest.mark.django_db
def test_delete_message_permission_denied(message, inbox_data):
    with pytest.raises(PermissionError):
        MessageService.delete_message(message, "not the owner", "wrong secret")


@pytest.mark.django_db
def test_delete_message_wrong_owner(message, inbox_data):
    with pytest.raises(PermissionError):
        MessageService.delete_message(
            message, "not_the_owner", inbox_data["secret"]
        )


@pytest.mark.django_db
def test_delete_message_wrong_secret(message, inbox_data):
    with pytest.raises(PermissionError):
        MessageService.delete_message(message, inbox_data["owner"], "wrong_secret")

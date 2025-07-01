from django.db.models import QuerySet

from settings import ERR_EXPIRED_INBOX, ERR_SIGNATURE_REQUIRED
from feedback_api.models.inbox import Inbox
from feedback_api.models.message import Message
from feedback_api.services.inbox import InboxService


class MessageService:
    @staticmethod
    def add_message_to_inbox(inbox: Inbox, body: str, signature: str) -> Message:
        if InboxService.is_expired(inbox):
            raise ValueError(ERR_EXPIRED_INBOX)
        if not inbox.allow_anonymous and not signature:
            raise ValueError(ERR_SIGNATURE_REQUIRED)
        return Message.objects.create(inbox=inbox, body=body, signature=signature)

    @staticmethod
    def get_messages_for_inbox(inbox: Inbox) -> QuerySet[Message]:
        return Message.objects.filter(inbox=inbox)

    @staticmethod
    def get_message_by_id(message_id: int) -> Message:
        return Message.objects.get(id=message_id)

    @staticmethod
    def delete_message(message: Message, username: str, secret: str) -> None:
        if not InboxService.owner_matches(message.inbox, username, secret):
            raise PermissionError("You are not the owner of this inbox.")
        message.delete()
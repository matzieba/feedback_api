from feedback_api.models.message import Message
from feedback_api.constants import ERR_EXPIRED_INBOX, ERR_SIGNATURE_REQUIRED
from feedback_api.services.inbox import InboxService

class MessageService:
    @staticmethod
    def add_message_to_inbox(inbox, body, signature):
        if InboxService.is_expired(inbox):
            raise ValueError(ERR_EXPIRED_INBOX)
        if not inbox.allow_anonymous and not signature:
            raise ValueError(ERR_SIGNATURE_REQUIRED)
        return Message.objects.create(inbox=inbox, body=body, signature=signature)
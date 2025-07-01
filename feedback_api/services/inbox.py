from django.utils import timezone

from settings import ERR_CANNOT_EDIT_TOPIC
from feedback_api.helpers import verify_tripcode
from feedback_api.models.inbox import Inbox


class InboxService:
    @staticmethod
    def owner_matches(inbox: Inbox, username: str, secret: str) -> bool:
        return verify_tripcode(inbox.signature, username, secret)

    @staticmethod
    def is_expired(inbox: Inbox) -> bool:
        return timezone.now() >= inbox.expiration_date

    @staticmethod
    def replies_count(inbox: Inbox) -> int:
        return inbox.messages.count()

    @staticmethod
    def can_edit_topic(inbox: Inbox) -> bool:
        return inbox.messages.count() == 0

    @staticmethod
    def change_topic(inbox: Inbox, new_topic: str, username: str, secret: str) -> Inbox:
        if not InboxService.owner_matches(inbox, username, secret):
            raise PermissionError(ERR_CANNOT_EDIT_TOPIC)
        if not InboxService.can_edit_topic(inbox):
            raise PermissionError(ERR_CANNOT_EDIT_TOPIC)
        inbox.topic = new_topic
        inbox.save(update_fields=["topic"])
        return inbox
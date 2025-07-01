from django.utils import timezone
from feedback_api.helpers import verify_tripcode
from feedback_api.constants import ERR_NOT_OWNER, ERR_CANNOT_EDIT_TOPIC, ERR_EXPIRED_INBOX

class InboxService:
    @staticmethod
    def owner_matches(inbox, username, secret):
        return verify_tripcode(inbox.signature, username, secret)

    @staticmethod
    def is_expired(inbox):
        return timezone.now() >= inbox.expiration_date

    @staticmethod
    def replies_count(inbox):
        return inbox.messages.count()

    @staticmethod
    def can_edit_topic(inbox):
        return inbox.messages.count() == 0

    @staticmethod
    def change_topic(inbox, new_topic, username, secret):
        if not InboxService.owner_matches(inbox, username, secret):
            raise PermissionError(ERR_NOT_OWNER)
        if not InboxService.can_edit_topic(inbox):
            raise ValueError(ERR_CANNOT_EDIT_TOPIC)
        inbox.topic = new_topic
        inbox.save(update_fields=["topic"])
        return inbox
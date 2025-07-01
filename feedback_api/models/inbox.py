import uuid
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from feedback_api.helpers import verify_tripcode


class Inbox(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=250)
    signature = models.CharField(max_length=128)  # tripcode string (owner signature)
    expiration_date = models.DateTimeField()
    allow_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() >= self.expiration_date

    @property
    def replies_count(self):
        return self.messages.count()

    @property
    def can_edit_topic(self):
        return self.replies_count == 0

    def owner_matches(self, username, secret):
        return verify_tripcode(self.signature, username, secret)

    def change_topic(self, new_topic, username, secret):
        if not self.owner_matches(username, secret):
            raise PermissionError("Only the owner can change the topic")
        if not self.can_edit_topic:
            raise ValueError("Cannot edit topic after replies posted.")
        self.topic = new_topic
        self.save(update_fields=["topic"])
        return self

    def get_replies_if_owner(self, username, secret):
        if not self.owner_matches(username, secret):
            raise PermissionError("Forbidden: Credentials don't match owner.")
        return self.messages.order_by("created_at")

    def __str__(self):
        return f"Inbox({self.topic}, ID={self.id})"

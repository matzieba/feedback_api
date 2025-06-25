import uuid
from model_utils.models import TimeStampedModel

from django.db import models
from django.utils import timezone

class Inbox(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=250)
    signature = models.CharField(max_length=128)  # tripcode string
    expiration_date = models.DateTimeField()
    allow_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        return timezone.now() >= self.expiration_date

    @property
    def replies_count(self) -> int:
        return self.messages.count()

    def can_edit_topic(self) -> bool:
        return self.replies_count == 0

    def __str__(self):
        return f"Inbox({self.topic}, ID={self.id})"
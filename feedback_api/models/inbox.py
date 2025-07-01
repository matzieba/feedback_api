import uuid
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from feedback_api.helpers import verify_tripcode


class Inbox(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=250)
    signature = models.CharField(max_length=128)
    expiration_date = models.DateTimeField()
    allow_anonymous = models.BooleanField(default=True)

    def __str__(self):
        return f"Inbox({self.topic}, ID={self.id})"

from django.db import models
from model_utils.models import TimeStampedModel


class Message(TimeStampedModel):
    inbox = models.ForeignKey(
        "feedback_api.Inbox", related_name="messages", on_delete=models.CASCADE
    )
    body = models.TextField()
    signature = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"Message({self.inbox_id}, at={self.created})"

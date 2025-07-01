from rest_framework import serializers
from feedback_api.models.message import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    body = serializers.CharField(max_length=1000)
    signature = serializers.CharField(max_length=256, allow_blank=True, required=False)

    class Meta:
        model = Message
        fields = ["body", "signature"]


class MessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "body", "signature", "created"]

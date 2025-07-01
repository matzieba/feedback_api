from rest_framework import serializers
from feedback_api.models.message import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["body", "signature"]


class MessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "body", "signature", "created"]

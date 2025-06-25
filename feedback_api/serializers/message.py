from rest_framework import serializers

from feedback_api.helpers import verify_tripcode
from feedback_api.models.message import Message

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['body', 'signature']  # signature may be null

    def validate(self, attrs):
        inbox = self.context['inbox']
        if inbox.is_expired():
            raise serializers.ValidationError("This inbox has expired.")
        if not inbox.allow_anonymous and not attrs.get('signature'):
            raise serializers.ValidationError("Signature required for non-anonymous inbox.")
        return attrs

    def create(self, validated_data):
        inbox = self.context['inbox']
        return Message.objects.create(inbox=inbox, **validated_data)

class MessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "body", "signature", "created_at"]

class InboxEditTopicSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=250)
    username = serializers.CharField()
    secret = serializers.CharField()

    def validate(self, attrs):
        inbox = self.context['inbox']
        if not verify_tripcode(inbox.signature, attrs["username"], attrs["secret"]):
            raise serializers.ValidationError("Forbidden: Credentials don't match owner.")
        if inbox.replies_count > 0:
            raise serializers.ValidationError("Cannot edit topic after replies posted.")
        return attrs

    def save(self):
        inbox = self.context['inbox']
        inbox.topic = self.validated_data["topic"]
        inbox.save()
        return inbox
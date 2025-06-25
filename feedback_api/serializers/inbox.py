from rest_framework import serializers

from feedback_api.helpers import make_tripcode
from feedback_api.models import Inbox


class InboxCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    secret = serializers.CharField(write_only=True)

    class Meta:
        model = Inbox
        fields = [
            'id', 'topic', 'expiration_date', 'allow_anonymous',
            'username', 'secret',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        username = validated_data.pop('username')
        secret = validated_data.pop('secret')
        tripcode = make_tripcode(username, secret)
        return Inbox.objects.create(signature=tripcode, **validated_data)

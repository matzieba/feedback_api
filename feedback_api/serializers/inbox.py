from rest_framework import serializers
from feedback_api.helpers import make_tripcode
from feedback_api.models.inbox import Inbox
from feedback_api.validators import validate_secret, validate_username


class InboxCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, validators=[validate_username])
    secret = serializers.CharField(write_only=True, validators=[validate_secret])

    class Meta:
        model = Inbox
        fields = [
            "id",
            "topic",
            "expiration_date",
            "allow_anonymous",
            "username",
            "secret",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        secret = validated_data.pop("secret")
        tripcode = make_tripcode(username, secret)
        return Inbox.objects.create(signature=tripcode, **validated_data)


class InboxPublicSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Inbox
        fields = ["id", "topic", "expiration_date", "allow_anonymous", "owner_name"]

    def get_owner_name(self, obj):
        if obj.signature and "!" in obj.signature:
            return obj.signature.split("!")[0]
        return None

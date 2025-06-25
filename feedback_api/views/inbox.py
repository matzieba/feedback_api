from rest_framework import viewsets, mixins
from feedback_api.models.inbox import Inbox
from feedback_api.serializers.inbox import (
    InboxCreateSerializer,
    InboxPublicSerializer,
)

class InboxViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Inbox.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return InboxCreateSerializer
        return InboxPublicSerializer

# TODO revise for privacy, add black
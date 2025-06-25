from rest_framework import generics
from ..models.inbox import Inbox
from ..serializers.inbox import InboxCreateSerializer

class InboxCreateAPIView(generics.CreateAPIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxCreateSerializer

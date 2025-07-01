from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from feedback_api.models.inbox import Inbox
from feedback_api.serializers.inbox import InboxCreateSerializer, InboxPublicSerializer
from feedback_api.serializers.message import MessageReadSerializer
from feedback_api.permissions import IsInboxOwner
from feedback_api.services.inbox import InboxService

class InboxViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Inbox.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return InboxCreateSerializer
        return InboxPublicSerializer

class InboxRepliesAPIView(APIView):
    permission_classes = [IsInboxOwner]

    def post(self, request, inbox_pk):
        """
        Returns inbox replies for the owner.
        Unusual: Listing is done via POST to allow passing credentials.
        """
        inbox = get_object_or_404(Inbox, pk=inbox_pk)
        messages = inbox.messages.order_by("created")
        serializer = MessageReadSerializer(messages, many=True)
        return Response(serializer.data)

class InboxEditTopicAPIView(APIView):
    permission_classes = [IsInboxOwner]

    def post(self, request, inbox_pk):
        inbox = get_object_or_404(Inbox, pk=inbox_pk)
        new_topic = request.data.get("topic")
        try:
            InboxService.change_topic(
                inbox,
                new_topic,
                username=request.data["username"],
                secret=request.data["secret"],
            )
        except (ValueError, PermissionError) as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "updated", "topic": inbox.topic})
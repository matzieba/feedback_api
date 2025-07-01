from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from feedback_api.models import Inbox
from feedback_api.serializers.message import (
    MessageReadSerializer,
    MessageCreateSerializer,
)
from feedback_api.services.message import MessageService

class MessageCreateAPIView(APIView):
    def post(self, request, inbox_pk):
        inbox = get_object_or_404(Inbox, pk=inbox_pk)
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            message = MessageService.add_message_to_inbox(
                inbox,
                serializer.validated_data["body"],
                serializer.validated_data.get("signature"),
            )
        except ValueError as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            MessageReadSerializer(message).data, status=status.HTTP_201_CREATED
        )
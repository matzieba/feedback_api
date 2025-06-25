from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback_api.helpers import verify_tripcode
from feedback_api.models.inbox import Inbox
from feedback_api.serializers.message import MessageCreateSerializer, MessageReadSerializer, InboxEditTopicSerializer


class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer

    def get_inbox(self):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Inbox, pk=self.kwargs.get("inbox_pk"))

    def create(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        serializer = self.get_serializer(data=request.data, context={"inbox": inbox})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)



class InboxRepliesAPIView(APIView):

    def post(self, request, inbox_pk):
        user = request.data.get("username")
        secret = request.data.get("secret")
        inbox = Inbox.objects.filter(pk=inbox_pk).first()
        if not inbox:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not (user and secret):
            return Response({"detail": "Missing credentials."}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_tripcode(inbox.signature, user, secret):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        messages = inbox.messages.all().order_by("created_at")
        ser = MessageReadSerializer(messages, many=True)
        return Response(ser.data)


class InboxEditTopicAPIView(APIView):
    def post(self, request, inbox_pk):
        from feedback_api.models.inbox import Inbox
        inbox = Inbox.objects.filter(pk=inbox_pk).first()
        if not inbox:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        ser = InboxEditTopicSerializer(data=request.data, context={'inbox': inbox})
        if ser.is_valid():
            ser.save()
            return Response({"status": "updated", "topic": inbox.topic})
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
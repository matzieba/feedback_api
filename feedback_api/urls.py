# feedback_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feedback_api.views.inbox import (
    InboxViewSet,
    InboxRepliesAPIView,
    InboxEditTopicAPIView,
)
from feedback_api.views.message import MessageCreateAPIView

router = DefaultRouter()
router.register(r"inboxes", InboxViewSet, basename="inbox")

urlpatterns = [
    # List, Retrieve, and Create inboxes
    path("", include(router.urls)),
    # Reply read: only owner can list replies (POST for credentials)
    path(
        "inboxes/<uuid:inbox_pk>/replies/",
        InboxRepliesAPIView.as_view(),
        name="inbox-replies",
    ),
    # Edit topic (only owner, only before replies)
    path(
        "inboxes/<uuid:inbox_pk>/edit-topic/",
        InboxEditTopicAPIView.as_view(),
        name="inbox-edit-topic",
    ),
    # Post messages (anyone)
    path(
        "inboxes/<uuid:inbox_pk>/messages/",
        MessageCreateAPIView.as_view(),
        name="inbox-messages",
    ),
]

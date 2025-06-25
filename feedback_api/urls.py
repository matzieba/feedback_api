from django.urls import path
from rest_framework.routers import DefaultRouter

from feedback_api.views.inbox import InboxViewSet
from feedback_api.views.message import MessageCreateAPIView, InboxRepliesAPIView, InboxEditTopicAPIView

router = DefaultRouter()
router.register(r'api/inboxes', InboxViewSet, basename='inbox')

urlpatterns = router.urls

urlpatterns += [
    path('api/inboxes/<uuid:inbox_pk>/messages/', MessageCreateAPIView.as_view(), name='message-create'),
    path('api/inboxes/<uuid:inbox_pk>/replies/', InboxRepliesAPIView.as_view(), name='inbox-replies'),
    path("api/inboxes/<uuid:inbox_pk>/edit-topic/", InboxEditTopicAPIView.as_view(), name="inbox-edit-topic"),

]
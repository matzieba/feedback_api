from django.urls import include, path, re_path

from .views.inbox import InboxCreateAPIView

api_urls = [
    path("inboxes/", InboxCreateAPIView.as_view(), name="inbox-create"),
]

urlpatterns = [
    re_path(r"api/", include(api_urls)),
]

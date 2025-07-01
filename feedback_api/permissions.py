from rest_framework.permissions import BasePermission
from feedback_api.models import Inbox


class IsInboxOwner(BasePermission):

    message = "Forbidden: you are not the owner."

    def has_permission(self, request, view):
        inbox_pk = view.kwargs.get("inbox_pk")
        if not inbox_pk:
            return False
        username = request.data.get("username") or request.query_params.get("username")
        secret = request.data.get("secret") or request.query_params.get("secret")
        if not (username and secret):
            return False
        try:
            inbox = Inbox.objects.get(pk=inbox_pk)
        except Inbox.DoesNotExist:
            return False
        return inbox.owner_matches(username, secret)

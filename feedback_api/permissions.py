from rest_framework.permissions import BasePermission

from feedback_api.services.inbox import InboxService


class IsInboxOwner(BasePermission):
    message = "Forbidden: you are not the owner."

    def has_object_permission(self, request, view, obj):
        username = request.data.get("username")
        secret = request.data.get("secret")
        if not (username and secret):
            return False
        return InboxService.owner_matches(obj, username, secret)
from feedback_api.models.message import Message


def add_message_to_inbox(inbox, body, signature):
    if inbox.is_expired:
        raise ValueError("This inbox has expired.")
    if not inbox.allow_anonymous and not signature:
        raise ValueError("Signature required for non-anonymous inbox.")
    return Message.objects.create(inbox=inbox, body=body, signature=signature)

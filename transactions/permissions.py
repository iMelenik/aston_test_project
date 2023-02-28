from rest_framework import permissions

from transactions.models import Transaction
from users.models import UserProfile


class TransactionOwner(permissions.BasePermission):
    """
    Custom permission to allow only transaction owner to read/edit it.
    """
    def has_object_permission(self, request, view, obj: Transaction):
        auth_user = UserProfile.objects.get(user=request.user)
        sender_owner = obj.sender.user
        receiver_owner = obj.receiver.user
        return True if auth_user in (sender_owner, receiver_owner) else False
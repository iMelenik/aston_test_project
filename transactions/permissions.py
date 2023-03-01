from rest_framework import permissions

from transactions.models import Transaction
from users.models import UserProfile
from wallets.models import Wallet


class IsTransactionOwner(permissions.BasePermission):
    """
    Custom permission to allow only transaction owner to read it.
    """
    def has_object_permission(self, request, view, obj: Transaction) -> bool:
        auth_user = UserProfile.objects.get(user=request.user)
        sender_owner = obj.sender.user
        receiver_owner = obj.receiver.user
        return auth_user in (sender_owner, receiver_owner)

    def has_permission(self, request, view):
        auth_user = UserProfile.objects.get(user=request.user)
        wallet = Wallet.objects.get(name=request.path.split('/')[-2])
        return wallet.user == auth_user

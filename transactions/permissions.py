from rest_framework import permissions

from transactions.models import Transaction
from users.models import UserProfile
from wallets.models import Wallet


class IsTransactionOwner(permissions.BasePermission):
    """
    Custom permission to allow only transaction owner read it.
    """
    def has_object_permission(self, request, view, obj: Transaction) -> bool:
        if request.user.is_anonymous:
            return False
        auth_user = UserProfile.objects.get(user=request.user)
        sender_owner = obj.sender.user
        receiver_owner = obj.receiver.user
        return auth_user in (sender_owner, receiver_owner)

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        auth_user = UserProfile.objects.get(user=request.user)
        transaction_id = request.path.split('/')[-2]
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return False
        return auth_user in (transaction.sender.user, transaction.receiver.user)


class IsWalletOwner(permissions.BasePermission):
    """
    Custom permission to allow only wallet owner read it.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        auth_user = UserProfile.objects.get(user=request.user)
        wallet_name = request.path.split('/')[-2]
        try:
            wallet = Wallet.objects.get(name=wallet_name)
        except Wallet.DoesNotExist:
            return False
        return wallet.user == auth_user

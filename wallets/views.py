from django.db.models import QuerySet
from rest_framework import viewsets, permissions, status, serializers

from users.models import UserProfile
from .models import Wallet
from .serializers import WalletSerializer


# Create your views here.
class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self) -> QuerySet:
        """
        Only current user's wallets are seen
        """
        user = UserProfile.objects.get(user=self.request.user)
        return Wallet.get_all_user_wallets(user)

    def perform_create(self, serializer) -> None:
        """
        checks if user don't have more than 5 wallets and
        sets bonus from bank (if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00);
        """
        user = UserProfile.objects.get(user=self.request.user)
        if Wallet.get_user_wallets_number(user) < 5:
            balance = 100 if serializer.validated_data['currency'] == 'RUB' else 3
            serializer.save(
                user=user,
                balance=balance
            )
        else:
            raise serializers.ValidationError("Only 5 wallets are allowed.")



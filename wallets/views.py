from random import choices
from string import ascii_uppercase, digits

from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.exceptions import ParseError

from users.models import UserProfile
from .models import Wallet
from .serializers import WalletSerializer


# Create your views here.
class WalletViewSet(viewsets.ModelViewSet):
    """
    Доделать:
    Для чтения GET только свои кошельки?
    Для удаления DELETE только свой кошелек?
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'name'

    def perform_create(self, serializer):
        """
        checks that user don't have more than 5 wallets;
        sets bonus from bank (if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00);
        """
        user = UserProfile.objects.get(user=self.request.user)
        if user.get_wallets_number() < 5:
            balance = 100 if serializer.validated_data['currency'] == 'RUB' else 3
            serializer.save(
                user=user,
                balance=balance
            )
        else:
            raise serializers.ValidationError("Only 5 wallets are allowed.")



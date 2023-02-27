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
    У пользователя не более 5 кошельков
    Для создания POST только type и currency
    Для чтения GET только свои кошельки?
    Для удаления DELETE только свой кошелек

    PUT PATCH NOT ALLOWED
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'name'

    def perform_create(self, serializer):
        """
        generates unique name on creation;
        checks that user don't have more than 5 wallets;
        sets bonus from bank (if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00);
        """
        user = UserProfile.objects.get(user=self.request.user)
        if user.get_wallets_number() < 5:
            name = self.__unique_wallet_name_generator()
            balance = 100 if serializer.validated_data['currency'] == 'RUB' else 3
            serializer.save(
                name=name,
                user=user,
                balance=balance
            )
        raise serializers.ValidationError("Only 5 wallets are allowed.")

    def __unique_wallet_name_generator(self) -> str:
        """generate unique random 8 symbols of latin alphabet and digits. Example: MO72RTX3"""
        name = ''.join(choices(ascii_uppercase + digits, k=8))
        try:
            Wallet.objects.get(name=name)
        except Wallet.DoesNotExist:
            return name
        else:
            self.__unique_wallet_name_generator()

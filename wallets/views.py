from random import choices
from string import ascii_uppercase, digits

from django.shortcuts import render
from rest_framework import viewsets, permissions
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

    # def perform_create(self, serializer):
    #     """
    #     generates unique name on creation;
    #     checks that user don't have more than 5 wallets;
    #     sets bonus from bank (if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00);
    #     """
    #     if not self.name:
    #         name = self.__unique_wallet_name_generator()
    #     user = self.request.user
    #
    #     serializer.save(
    #         name=user,
    #     )

    def __unique_wallet_name_generator(self) -> str:
        """generate unique random 8 symbols of latin alphabet and digits. Example: MO72RTX3"""
        name = ''.join(choices(ascii_uppercase + digits, k=8))
        try:
            Wallet.objects.get(name=name)
        except Wallet.DoesNotExist:
            return name
        else:
            self.__unique_wallet_name_generator()

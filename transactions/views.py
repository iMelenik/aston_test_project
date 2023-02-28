from decimal import Decimal

from django.db import transaction
from django.db.models import QuerySet, F
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.permissions import TransactionOwner
from transactions.serializers import TransactionSerializer
from users.models import UserProfile
from wallets.models import Wallet


class TransactionListView(generics.ListCreateAPIView):
    """
    create new transaction and get list of current user's transactions
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        return queryset of current user transactions
        """
        user = UserProfile.objects.get(user=self.request.user)
        return Transaction.get_all_user_transactions(user)

    # @transaction.atomic
    def perform_create(self, serializer):
        """
        update wallets balance and set transaction status True
        """
        transfer_amount = serializer.validated_data['transfer_amount']
        commission = serializer.validated_data['commission']

        sender = Wallet.objects.select_for_update().get(name=serializer.validated_data['sender'].name)
        receiver = Wallet.objects.select_for_update().get(name=serializer.validated_data['receiver'].name)

        with transaction.atomic():
            sender.balance -= transfer_amount + commission
            sender.save()

            receiver.balance += transfer_amount
            receiver.save()

            serializer.save(status='PAID')


class TransactionDetailView(generics.RetrieveAPIView):
    """
    retrieve single transaction by id
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [TransactionOwner]


class TransactionWalletView(APIView):
    """
    retrieve all transactions for current wallet
    """
    permission_classes = [TransactionOwner]

    def get_wallet(self, name: str) -> Wallet:
        """get wallet obj from name"""
        wallet = get_object_or_404(Wallet, name=name)
        return wallet

    def get(self, request, name):
        wallet = self.get_wallet(name)
        qs = Transaction.get_all_wallet_transactions(wallet)
        serializer = TransactionSerializer(qs, many=True)
        return Response(serializer.data)

from decimal import Decimal
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionListView(generics.ListCreateAPIView):
    """
    create new and get list of current user's transactions
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        """
        set commission: 0% if both wallets belong to one user, else 10%
        """
        sender = serializer.validated_data['sender']
        receiver = serializer.validated_data['receiver']
        amount = serializer.validated_data['transfer_amount']
        if sender == receiver:
            commission = 0
        else:
            commission = amount * Decimal('0.1')
        serializer.save(commission=commission)


class TransactionDetailView(generics.RetrieveAPIView):
    """
    retrieve transaction by id
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionWalletView(APIView):
    """
    retrieve all transactions for current wallet
    """
    def get(self, request, name):
        pass

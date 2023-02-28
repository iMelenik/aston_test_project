from django.shortcuts import render
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

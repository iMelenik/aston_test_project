from decimal import Decimal

from rest_framework import serializers

from wallets.models import Wallet
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='name', queryset=Wallet.objects.all())
    receiver = serializers.SlugRelatedField(slug_field='name', queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount', 'commission', 'status', 'timestamp']
        read_only_fields = ['status']

    def validate(self, data):
        if data.get('transfer_amount') <= 0:
            raise serializers.ValidationError("Transfer amount can't be less or equal zero.")
        sender = data.get('sender')
        receiver = data.get('receiver')
        self.same_sender_receiver_validator(sender, receiver)
        self.sender_receiver_currency_validator(sender, receiver)
        commission = self.is_sender_have_enough(sender, receiver, data.get('transfer_amount'))
        data['commission'] = commission
        return data

    @staticmethod
    def same_sender_receiver_validator(sender: Wallet, receiver: Wallet) -> None:
        """
        checks if sender and receiver are not the same
        """
        if sender == receiver:
            raise serializers.ValidationError("You cant send and receive on the same wallet.")

    @staticmethod
    def sender_receiver_currency_validator(sender: Wallet, receiver: Wallet) -> None:
        """
        checks if both wallets are same currency
        """
        if sender.currency != receiver.currency:
            raise serializers.ValidationError(f"Wallets have different currency. "
                                              f"Receiver currency is {receiver.currency}.")

    @staticmethod
    def is_sender_have_enough(sender: Wallet, receiver: Wallet, amount: Decimal) -> Decimal:
        """
        checks if sender have enough balance for transaction, calculates commission
        """
        if sender.user == receiver.user:
            commission = 0
        else:
            commission = amount * Decimal('0.1')

        if (sender.balance - amount - commission) < Decimal(0):
            raise serializers.ValidationError("Not enough money on wallet for transaction.")

        return commission

from rest_framework import serializers

from wallets.models import Wallet
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount', 'commission', 'status', 'timestamp']
        read_only_fields = ['status']
        # lookup_field = 'name'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'name'}
        # }

    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')
        self.same_sender_receiver_validator(sender, receiver)
        self.sender_receiver_currency_validator(sender, receiver)
        return data

    @staticmethod
    def same_sender_receiver_validator(sender: Wallet, receiver: Wallet) -> None:
        """
        checks if sender and receiver are the same
        """
        if sender == receiver:
            raise serializers.ValidationError("You cant send and receive on the same wallet.")

    @staticmethod
    def sender_receiver_currency_validator(sender: Wallet, receiver: Wallet) -> None:
        """
        checks if wallets are the same currency
        """
        if sender.currency != receiver.currency:
            raise serializers.ValidationError(f"Wallets have different currency. "
                                              f"Receiver currency is {receiver.currency}.")

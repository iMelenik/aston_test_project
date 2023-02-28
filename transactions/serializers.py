from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    # sender = serializers.HyperlinkedIdentityField(view_name='wallets:detail', lookup_field='name')
    # receiver = serializers.HyperlinkedIdentityField(view_name='wallets:detail', lookup_field='name')

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount', 'commission', 'status', 'timestamp']
        read_only_fields = ['status']
        # lookup_field = 'name'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'name'}
        # }

    def check_if_same_wallets(self):
        """
        checks if sender and receiver are the same
        """
        pass

    def check_wallets_currency(self):
        """
        checks if wallets are the same currency
        """
        pass

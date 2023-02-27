# from rest_framework import serializers
# from .models import Transaction
#
#
# class TransactionSerializer(serializers.ModelSerializer):
#     # sender = serializers.HyperlinkedIdentityField(view_name='wallets:detail', lookup_field='name')
#     # receiver = serializers.HyperlinkedIdentityField(view_name='wallets:detail', lookup_field='name')
#
#     class Meta:
#         model = Transaction
#         fields = ['id', 'name', 'user', 'type', 'currency', 'balance', 'created_on', 'modified_on']
#         read_only_fields = ['balance']
#         # lookup_field = 'name'
#         # extra_kwargs = {
#         #     'url': {'lookup_field': 'name'}
#         # }
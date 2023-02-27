from rest_framework import serializers

from users.models import UserProfile
from .models import Wallet


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='users:detail', queryset=UserProfile.objects.all())

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'user', 'type', 'currency', 'balance', 'created_on', 'modified_on']

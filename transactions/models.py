from django.db import models

from wallets.models import Wallet


# Create your models here.
class Transaction(models.Model):
    """
    Проверки
    - комиссия между своими кошельками 0, чужими 10%
    - доступности баланса, в т.ч. с комиссией
    - разные кошельки, одинаковые валюты
    """
    sender = models.ForeignKey(Wallet, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(Wallet, on_delete=models.SET_NULL)
    transfer_amount = models.DecimalField(decimal_places=2, max_digits=15)
    commission = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True, editable=False)
    status = models.CharField(choices=['PAID', 'FAILED'], default='FAILED')
    timestamp = models.DateTimeField(auto_now_add=True)

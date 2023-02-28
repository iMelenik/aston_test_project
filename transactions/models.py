from django.db import models

from wallets.models import Wallet


# Create your models here.
class Transaction(models.Model):
    objects = models.Manager()

    sender = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='trans_sender')
    receiver = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='trans_receiver')
    transfer_amount = models.DecimalField(decimal_places=2, max_digits=15)
    commission = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True, editable=False)
    status = models.CharField(choices=[('PAID', 'P'), ('FAILED', 'F')], default='FAILED', max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

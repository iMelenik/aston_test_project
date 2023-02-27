from django.db import models

from users.models import UserProfile


# Create your models here.
class Wallet(models.Model):
    TYPES_CHOICES = [
        ('VISA', 'Visa'),
        ('MC', 'Mastercard')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RUB', 'RUB'),
    ]

    objects = models.Manager()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wallet')

    name = models.CharField(unique=True, null=True, blank=True, max_length=8, editable=False)
    type = models.CharField(choices=TYPES_CHOICES, max_length=10)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    balance = models.DecimalField(decimal_places=2, max_digits=15)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Кошелек {self.type} с валютой {self.currency}."

    def get_sender_transactions(self):
        qs = self.trans_sender.all()
        if qs.exists():
            return qs
        # return "С данного кошелька ни разу не отправляли деньги."

    def get_receiver_transactions(self):
        qs = self.trans_receiver.all()
        if qs.exists():
            return qs
        # return "На данный кошелек ни разу не отправляли деньги."

    def get_all_wallet_transactions(self):
        qs = self.get_sender_transactions() | self.get_receiver_transactions()
        if qs.exists():
            return qs
        # return "С данным кошельком не выполнялось никаких операций."

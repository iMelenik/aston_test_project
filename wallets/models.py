from random import choices
from string import ascii_uppercase, digits

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
        return f"Кошелек {self.name} с валютой {self.currency}."

    def save(self, *args, **kwargs):
        """generates name on creation"""
        if not self.name:
            self.__unique_wallet_name_generate()
        super().save(*args, **kwargs)

    def __unique_wallet_name_generate(self) -> None:
        """generate unique random 8 symbols of latin alphabet and digits. Example: MO72RTX3"""
        name = ''.join(choices(ascii_uppercase + digits, k=8))
        try:
            Wallet.objects.get(name=name)
        except Wallet.DoesNotExist:
            self.name = name
        else:
            self.__unique_wallet_name_generate()



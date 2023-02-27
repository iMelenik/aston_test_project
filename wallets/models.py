from random import choices
from string import ascii_uppercase, digits

from django.db import models


# Create your models here.
class Wallet(models.Model):
    objects = models.Manager()

    name = models.CharField(unique=True, null=True, blank=True, max_length=8)
    type = models.CharField(choices=('Visa', 'Mastercard'), default='Visa')
    currency = models.CharField(choices=('USD', 'EUR', 'RUB'), default='RUB')
    balance = models.DecimalField(decimal_places=2)
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
        name = choices([ascii_uppercase, digits], k=8)
        try:
            Wallet.objects.get(name=name)
        except Wallet.DoesNotExist:
            self.name = name
        else:
            self.__unique_wallet_name_generate()



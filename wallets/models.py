from django.db import models


# Create your models here.
class Wallet(models.Model):
    objects = models.Manager()

    name = models.CharField(unique=True, null=True, blank=True, max_length=8)
    type = models.CharField(choices=['Visa', 'Mastercard'], default='Visa')
    currency = models.CharField(choices=['USD', 'EUR', 'RUB'], default='RUB')
    balance = models.DecimalField(decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Кошелек {self.name} с валютой {self.currency}."

    def save(self, *args, **kwargs):
        if not self.name:
            self.unique_wallet_name_generate()
        super().save(*args, **kwargs)

    @staticmethod
    def unique_wallet_name_generate():
        """generate unique random 8 symbols of latin alphabet and digits. Example: MO72RTX3"""
        pass


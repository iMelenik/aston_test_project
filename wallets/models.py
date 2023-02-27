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

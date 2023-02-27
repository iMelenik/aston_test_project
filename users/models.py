from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_all_user_wallets(self):
        qs = self.wallet.all()
        if qs.exists():
            return qs
        return "У данного пользователя не создано ни одного кошелька."

    def get_wallets_number(self):
        return self.wallet.count()

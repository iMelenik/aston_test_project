from django.conf import settings
from django.db import models

# Create your models here.
User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_all_user_wallets(self):
        qs = self.wallet_set.all()
        if qs.exists():
            return qs
        return "У данного пользователя не создано ни одного кошелька."

    def get_wallets_number(self):
        return self.wallet_set.count()

from django.db import models
from django.contrib.auth.models import User

from wallets.models import Wallet


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_all_user_wallets(self):
        pass

    def get_wallets_number(self):
        pass
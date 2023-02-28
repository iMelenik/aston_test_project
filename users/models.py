from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token


# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

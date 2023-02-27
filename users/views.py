from django.shortcuts import render
from rest_framework import generics

from .models import UserProfile
from .serializers import UserProfileSerializer


# Create your views here.
class UserLogin:
    pass


class UserLogout:
    pass


class UserRegister:
    pass


class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

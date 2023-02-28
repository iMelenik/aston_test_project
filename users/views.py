from django.contrib.auth import get_user_model, logout
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


# Create your views here.
class UserLoginView(ObtainAuthToken):
    """
    success login creates and returns token
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


class UserLogoutView(APIView):
    """
    Delete token and logout user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response('Successfully logout.')


class UserRegisterView(generics.CreateAPIView):
    """
    creates User and UserProfile models without token
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer


class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]

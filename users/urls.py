from django.urls import path, include
from rest_framework.authtoken import views

from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
]

urlpatterns += [
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('', UserListView.as_view(), name='list'),
]

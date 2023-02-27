from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    # path('login', UserLogin.as_view(), name='login'),
    # path('logout', UserLogout.as_view(), name='logout'),
    # path('register', UserRegister.as_view(), name='register'),
    path('<int:pk>/', UserDetail.as_view(), name='detail'),
    path('all', UserList.as_view(), name='list'),
]
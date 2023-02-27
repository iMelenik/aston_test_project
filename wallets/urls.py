from django.urls import path

app_name = 'wallets'
from .views import *

wallet_list = WalletViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

wallet_detail = WalletViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('list/', wallet_list, name='list'),
    path('<int:pk>/', wallet_detail, name='detail')
]
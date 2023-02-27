from django.urls import path

from .views import *


app_name = 'wallets'

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
    path('', wallet_list, name='list'),
    path('<slug:name>/', wallet_detail, name='detail')
]

from django.urls import path

app_name = 'transactions'

# wallet_list = WalletViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# wallet_detail = WalletViewSet.as_view({
#     'get': 'retrieve',
#     'delete': 'destroy'
# })

urlpatterns = [
    # path('', wallet_list, name='list'),
    # path('<slug:name>/', wallet_detail, name='detail')
]

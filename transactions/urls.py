from django.urls import path
from .views import *


app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction'),
    path('<str:name>/', TransactionWalletView.as_view(), name='wallet')
]

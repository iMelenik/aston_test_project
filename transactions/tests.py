from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from transactions.models import Transaction
from users.models import UserProfile
from wallets.models import Wallet

User = get_user_model()


class WalletViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='name1',
            password='pass1',
            email='tt1@tt.ru',
        )
        self.token_user1 = Token.objects.create(user=self.user1)
        self.userprof1 = UserProfile.objects.create(user=self.user1)
        self.wallet_1_usd1 = Wallet.objects.create(
            user=self.userprof1,
            type='Visa',
            currency='USD',
            balance=3
        )
        self.wallet_1_usd2 = Wallet.objects.create(
            user=self.userprof1,
            type='Visa',
            currency='USD',
            balance=3
        )
        self.transaction = Transaction.objects.create(
            sender=self.wallet_1_usd1,
            receiver=self.wallet_1_usd2,
            transfer_amount=0,
            commission=0,
        )

        self.user2 = User.objects.create_user(
            username='name2',
            password='pass2',
            email='tt2@tt.ru',
        )
        self.token_user2 = Token.objects.create(user=self.user2)
        self.userprof2 = UserProfile.objects.create(user=self.user2)
        self.wallet_2_usd1 = Wallet.objects.create(
            user=self.userprof2,
            type='Visa',
            currency='USD',
            balance=3
        )
        self.wallet_2_rub2 = Wallet.objects.create(
            user=self.userprof2,
            type='Visa',
            currency='RUB',
            balance=100
        )

    def test_transaction_list_view(self):
        """
        ALL: requires authentication, only owner
        GET: returns list of transactions from all owner's wallets
        POST: create new transaction
        """
        url = reverse('transactions:list')

        """unauthorized"""
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """not owner user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        """simple user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(url, {
            'sender': self.wallet_1_usd1.name,
            'receiver': self.wallet_1_usd2.name,
            'transfer_amount': Decimal(1),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

        """transfer amount greater than zero"""
        response = self.client.post(url, {
            'sender': self.wallet_1_usd1.name,
            'receiver': self.wallet_1_usd2.name,
            'transfer_amount': Decimal(0),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 2)

        """not same wallet check"""
        response = self.client.post(url, {
            'sender': self.wallet_1_usd1.name,
            'receiver': self.wallet_1_usd1.name,
            'transfer_amount': Decimal(0),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 2)

        """not same wallets currency check"""
        response = self.client.post(url, {
            'sender': self.wallet_1_usd2.name,
            'receiver': self.wallet_2_rub2.name,
            'transfer_amount': Decimal(0),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 2)

        """commission calculation check
        balance calculation and status check"""
        # print(self.wallet_1_usd1, self.wallet_1_usd1.balance)
        response = self.client.post(url, {
            'sender': self.wallet_1_usd1.name,
            'receiver': self.wallet_1_usd2.name,
            'transfer_amount': Decimal(1),
        }, format='json')
        self.assertEqual(response.data['commission'], '0.00')
        self.assertEqual(response.data['status'], 'PAID')
        # print(self.wallet_1_usd1, self.wallet_1_usd1.balance)
        sender = Wallet.objects.get(name=response.data['sender'])
        # print(sender, sender.balance)
        # WHY?!
        receiver = Wallet.objects.get(name=response.data['receiver'])
        self.assertEqual(sender.balance, Decimal(1))
        self.assertEqual(receiver.balance, Decimal(5))

    # def test_transaction_detail_view(self):
    #     """
    #     ALL: requires authentication, only owner
    #     GET: returns transaction detail
    #     POST: method not allowed
    #     """
    #     url = reverse('transactions:transaction', kwargs={'id': 1})
    #
    # def test_transaction_wallet_view(self):
    #     """
    #     ALL: requires authentication, only owner
    #     GET: returns all transactions for wallet
    #     POST: method not allowed
    #     """
    #     url = reverse('transactions:wallet', kwargs={'name': 123})

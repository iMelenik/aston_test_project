from decimal import Decimal
from time import sleep

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import UserProfile
from wallets.models import Wallet

User = get_user_model()


class WalletsUsageTestCase(APITestCase):
    """
    Creation generates unique name
    Filed "modified" auto updates
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )
        self.token_user = Token.objects.create(user=self.user)
        self.user_profile = UserProfile.objects.create(user=self.user)

        self.wallet = Wallet.objects.create(
            user=self.user_profile,
            type='Visa',
            currency='USD',
            balance=0,
        )

    def test_wallet_name_generation(self):
        self.assertEqual(len(self.wallet.name), 8)

    def test_wallet_field_modified(self):
        self.assertEqual(self.wallet.created_on, self.wallet.modified_on)
        sleep(0.00001)
        self.wallet.save()
        self.assertNotEqual(self.wallet.created_on, self.wallet.modified_on)


class WalletViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='name1',
            password='pass1',
            email='tt1@tt.ru',
        )
        self.token_user1 = Token.objects.create(user=self.user1)
        UserProfile.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            username='name2',
            password='pass2',
            email='tt2@tt.ru',
        )
        self.token_user2 = Token.objects.create(user=self.user2)

        self.wallet = Wallet.objects.create(
            user=UserProfile.objects.create(user=self.user2),
            type='Visa',
            currency='USD',
            balance=0
        )

    def test_wallets_list_view(self):
        """
        ALL: requires authentication, only owner
        GET: returns list of all owners wallets
        POST: create new wallet
        """
        url = reverse('wallets:list')

        """unauthorized"""
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """simple user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        """balance calculation check"""
        for currency in ('USD', 'RUB', 'EUR'):
            data = {
                'type': 'Visa',
                'currency': currency,
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Decimal(response.data['balance']),
                             3 if response.data['currency'] in ('EUR', 'USD') else 100)

        """max number of wallets check"""
        for i in range(6):
            data = {
                'type': 'Visa',
                'currency': 'RUB',
            }
            self.client.post(url, data, format='json')

        self.assertEqual(Wallet.objects.count(), 6)

        """not owner user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)

    def test_wallet_detail_view(self):
        """
        ALL: requires authentication, only owner
        GET: returns specific wallet
        POST: method not allowed
        DELETE: delete wallet
        """
        url = reverse('wallets:detail', kwargs={'name': self.wallet.name})

        """unauthorized"""
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """not owner user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """simple user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'http://testserver/wallets/'+self.wallet.name+'/')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(url, format='json')
        self.assertEqual(self.client.get(url, format='json').status_code, status.HTTP_404_NOT_FOUND)



from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import UserProfile
from wallets.models import Wallet

User = get_user_model()

"""
1) проверка создания Wallet
2) проверка полей:
    - уникальное имя
    - modified обновляется
    - автобаланс 3 евро/доллара или 100 рублей
3) проверка 5 кошельков
4) проверка удаления кошелька
"""


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
        self.wallet.save()
        self.assertNotEqual(self.wallet.created_on, self.wallet.modified_on)


class WalletViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )
        self.token_user = Token.objects.create(user=self.user1)
        UserProfile.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )
        self.token_user = Token.objects.create(user=self.user2)
        UserProfile.objects.create(user=self.user2)

    # def test_wallets_list_view(self):
    #     """
    #     ALL: requires authentication, only owner
    #     GET: returns list of all owners wallets
    #     POST: method not allowed
    #     """
    #     url = reverse('wallets:list')
    #     """unauthorized"""
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     """simple user"""
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
    #
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     def test_wallet_balance_calculation():
    #         """Field "balance" calculates correctly"""
    #         print(self.wallet.balance)
    #
    #     def test_wallet_number_allowed():
    #         """Only 5 wallets allowed for 1 user"""
    #         pass
    #
    #     test_wallet_balance_calculation()
    #     test_wallet_number_allowed()
    #
    # def test_wallet_detail_view(self):
    #     """
    #     ALL: requires authentication, only owner
    #     GET: returns specific wallet
    #     POST: method not allowed
    #     DELETE: delete wallet
    #     """
    #     url = reverse('wallets:detail')
    #     """unauthorized"""
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     """simple user"""
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
    #
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

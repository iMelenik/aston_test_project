from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import UserProfile

User = get_user_model()


class UserUsageTestCase(APITestCase):
    def test_registration(self):
        """
        GET: method not allowed
        POST: if models User and UserProfile successfully created
        """
        url = reverse('users:register')
        data = {
            'username': 'name',
            'password': 'pass',
            'password2': 'pass',
            'email': 'tt@tt.ru',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

        user = User.objects.get()

        self.assertEqual(user.username, 'name')
        self.assertEqual(user.email, 'tt@tt.ru')

        self.assertEqual(UserProfile.objects.get().user, user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login(self):
        """
        GET: method not allowed
        POST: sending username and password returns token
        """
        url = reverse('users:login')
        data = {
            'username': 'name',
            'password': 'pass',
        }

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        user = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], Token.objects.get(user=user).key)

    def test_logout(self):
        """
        ALL: requires authentication
        GET: method not allowed
        POST: successfully logout, token deleted
        """
        url = reverse('users:logout')

        """unauthorized"""
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """simple user"""
        user = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Successfully logout.')

        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)


class UserViewsTestCase(APITestCase):

    def setUp(self) -> None:
        self.simple_user = User.objects.create_user(
            username='name',
            password='pass',
            email='tt@tt.ru',
        )
        self.token_user = Token.objects.create(user=self.simple_user)
        UserProfile.objects.create(user=self.simple_user)

        self.admin = User.objects.create_user(
            username='admin',
            password='admin',
            email='admin@tt.ru',
        )
        self.admin.is_staff = True
        self.admin.save()
        self.token_admin = Token.objects.create(user=self.admin)
        UserProfile.objects.create(user=self.admin)

    def test_user_list_view(self):
        """
        ALL: requires authentication, only admin permission
        GET: returns list of all users
        POST: method not allowed
        """
        url = reverse('users:list')
        """unauthorized"""
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """simple user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        """admin user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), UserProfile.objects.count())

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_detail_view(self):
        """
        ALL: requires authentication
        GET: returns user by userprofile id
        POST: method not allowed
        """
        user_id = UserProfile.objects.get(user=self.simple_user).id
        url = reverse('users:detail', kwargs={'pk': user_id})

        """unauthorized"""
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        """simple user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user_id)

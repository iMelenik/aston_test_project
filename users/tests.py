from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import UserProfile
User = get_user_model()


class UserTestCase(APITestCase):
    """
    1) проверка создания User и UserProfile при регистрации
    2) проверка генерации токена при логине
    3) проверка удаления токена при логауте
    """

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
        pass

    def test_logout(self):
        pass

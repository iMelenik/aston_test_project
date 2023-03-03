import pytest
from decimal import Decimal

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token

from users.models import UserProfile
from wallets.models import Wallet

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_create(db, api_client):
    def create(name: str = 'abc', mail: str = 'a@b.c'):
        user = User.objects.create_user(
            username=name,
            password='pass',
            email=mail,
        )
        userprofile = UserProfile.objects.create(user=user)
        return user, userprofile

    return create


@pytest.fixture
def user_login(db, api_client):
    def login(user):
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return api_client

    return login


@pytest.fixture
def wallet_create(db, user_create, user_login):
    def create(currency, created_user):
        user, userprofile = created_user
        wallet = Wallet.objects.create(
            user=userprofile,
            type='Visa',
            currency=currency,
            balance=0
        )
        return wallet

    return create


@pytest.mark.unauthorized
@pytest.mark.django_db()
def test_unauthorized_list_view_get(api_client):
    url = reverse('wallets:list')

    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.unauthorized
@pytest.mark.django_db()
def test_unauthorized_list_view_post(api_client):
    url = reverse('wallets:list')

    response = api_client.post(url)
    assert response.status_code == 401


@pytest.mark.simple_user
@pytest.mark.django_db()
def test_user_list_view_get(user_create, user_login, wallet_create):
    url = reverse('wallets:list')

    user, userprofile = user_create('123', '1@1.1')
    api_client = user_login(user)

    response = api_client.get(url)
    assert response.status_code == 200

    user_wallet = wallet_create('USD', (user, userprofile))
    response = api_client.get(url)
    assert len(response.data) == 1


@pytest.mark.not_owner
@pytest.mark.django_db()
def test_not_owner_list_view_get(user_create, user_login, wallet_create):
    url = reverse('wallets:list')

    user, userprofile = user_create('123', '1@1.1')
    api_client = user_login(user)

    foreign_wallet1 = wallet_create('RUB', user_create('fw1', 'f@w.1'))
    response = api_client.get(url)
    assert len(response.data) == 0


@pytest.mark.simple_user
@pytest.mark.django_db()
def test_user_list_view_post(user_create, user_login):
    url = reverse('wallets:list')

    user, userprofile = user_create('123', '1@1.1')
    api_client = user_login(user)

    response = api_client.post(url)
    assert response.status_code == 400

    data = {
        'type': 'Visa',
        'currency': 'EUR',
    }
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert len(response.data['name'].split('/')[-2]) == 8

    response = api_client.get(url)
    assert len(response.data) == 1


@pytest.mark.parametrize(
    'currency, balance', [
        ('EUR', 3),
        ('RUB', 100),
        ('USD', 3),
    ]
)
@pytest.mark.simple_user
@pytest.mark.django_db()
def test_balance_calculation(user_create, user_login, currency, balance):
    url = reverse('wallets:list')

    user, userprofile = user_create('123', '1@1.1')
    api_client = user_login(user)

    data = {
        'type': 'Visa',
        'currency': currency,
    }
    response = api_client.post(url, data=data)
    assert Decimal(response.data['balance']) == balance


@pytest.mark.simple_user
@pytest.mark.django_db()
def test_allowed_wallets_number(user_create, user_login):
    url = reverse('wallets:list')

    user, userprofile = user_create('123', '1@1.1')
    api_client = user_login(user)

    data = {
        'type': 'Visa',
        'currency': 'EUR',
    }

    for i in range(5):
        api_client.post(url, data=data)
        response = api_client.get(url, data=data)
        assert len(response.data) == i + 1

    api_client.post(url, data=data)
    response = api_client.get(url, data=data)
    assert len(response.data) == 5


@pytest.mark.unauthorized
@pytest.mark.django_db()
def test_unauthorized_detail_view_get(api_client, user_create, wallet_create):
    wallet = wallet_create('RUB', user_create())
    url = reverse('wallets:detail', kwargs={'name': wallet.name})

    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.unauthorized
@pytest.mark.django_db()
def test_unauthorized_detail_view(api_client, user_create, wallet_create):
    wallet = wallet_create('RUB', user_create())
    url = reverse('wallets:detail', kwargs={'name': wallet.name})

    response = api_client.get(url)
    assert response.status_code == 401

    response = api_client.post(url)
    assert response.status_code == 401


@pytest.mark.simple_user
@pytest.mark.django_db()
def test_user_detail_view(user_create, wallet_create, user_login):
    user, userprofile = user_create()
    api_client = user_login(user)
    wallet = wallet_create('RUB', (user, userprofile))
    url = reverse('wallets:detail', kwargs={'name': wallet.name})

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'].split('/')[-2] == wallet.name

    response = api_client.post(url)
    assert response.status_code == 405


@pytest.mark.not_owner
@pytest.mark.django_db()
def test_not_owner_detail_view(user_create, wallet_create, user_login):
    user, userprofile = user_create()
    api_client = user_login(user)
    foreign_wallet = wallet_create('RUB', user_create('f2', 'f@f.f'))
    url = reverse('wallets:detail', kwargs={'name': foreign_wallet.name})

    response = api_client.get(url)
    assert response.status_code == 404

    response = api_client.post(url)
    assert response.status_code == 405

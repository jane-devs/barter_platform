import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from ads.models import Ad, ExchangeProposal
from constants import ConstStr


@pytest.fixture
def api_client():
    """Возвращает неаутентифицированный клиент API для тестирования."""
    return APIClient()


@pytest.fixture
def user1(db):
    """Создаёт и возвращает первого пользователя с username 'user1'."""
    return User.objects.create_user(username='user1', password='pass')


@pytest.fixture
def user2(db):
    """Создаёт и возвращает второго пользователя с username 'user2'."""
    return User.objects.create_user(username='user2', password='pass2')


@pytest.fixture
def auth_client(user1):
    """Возвращает клиент API, аутентифицированный как user1."""
    client = APIClient()
    client.force_authenticate(user=user1)
    return client


@pytest.fixture
def ad1(user1):
    """Создаёт и возвращает объявление, принадлежащее user1."""
    return Ad.objects.create(
        user=user1,
        title='Стол',
        description='Деревянный',
        category='furniture',
        condition='used'
    )


@pytest.fixture
def ad2(user2):
    """Создаёт и возвращает объявление, принадлежащее user2."""
    return Ad.objects.create(
        user=user2,
        title='Лампа',
        description='Светодиодная',
        category='electronics',
        condition='new'
    )


@pytest.fixture
def exchange_proposal(ad1, ad2):
    """
    Создаёт и возвращает предложение обмена
    от ad1 к ad2 со статусом PENDING.
    """
    return ExchangeProposal.objects.create(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment='Обмен?',
        status=ConstStr.PENDING
    )

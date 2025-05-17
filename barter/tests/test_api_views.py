import pytest
from ads.models import ExchangeProposal
from constants import ConstStr


@pytest.mark.django_db
def test_create_ad_api(auth_client, user1):
    """
    Проверяет успешное создание объявления через API.
    user1 нужен для аутентификации клиента.
    """
    response = auth_client.post('/api/ads/', {
        'title': 'Кресло',
        'description': 'Кожаное',
        'category': 'furniture',
        'condition': 'new'
    })

    assert response.status_code == 201, response.data


@pytest.mark.django_db
def test_get_ads_list(auth_client, ad1):
    """
    Проверяет получение списка объявлений через API.
    Должен вернуть как минимум объявление ad1.
    """
    response = auth_client.get('/api/ads/')
    results = response.data['results']
    assert len(results) == 1
    assert results[0]['title'] == ad1.title


@pytest.mark.django_db
def test_filter_ads_by_category(auth_client, ad1, ad2):
    """
    Проверяет фильтрацию объявлений по категории 'furniture'.
    В результате должен быть только один объект с категорией 'furniture'.
    """
    response = auth_client.get('/api/ads/?category=furniture')
    results = response.data['results']
    assert len(results) == 1
    assert results[0]['category'] == 'furniture'


@pytest.mark.django_db
def test_create_exchange_proposal(auth_client, ad1, ad2):
    """
    Проверяет создание предложения обмена от ad1 к ad2 через API.
    После запроса в базе должен появиться один объект ExchangeProposal.
    """
    response = auth_client.post('/api/proposals/', {
        'ad_sender': ad1.id,
        'ad_receiver': ad2.id,
        'comment': 'Обменяемся?'
    })
    assert response.status_code == 201
    assert ExchangeProposal.objects.count() == 1


@pytest.mark.django_db
def test_accept_proposal(api_client, user2, exchange_proposal):
    """
    Проверяет, что пользователь user2 может принять предложение обмена.
    Статус предложения должен измениться на 'accepted'.
    """
    api_client.force_authenticate(user=user2)
    response = api_client.post(
        f'/api/proposals/{exchange_proposal.id}/accept/')
    exchange_proposal.refresh_from_db()

    assert response.status_code == 200
    assert exchange_proposal.status == ConstStr.ACCEPTED


@pytest.mark.django_db
def test_reject_proposal(api_client, user2, exchange_proposal):
    """
    Проверяет, что пользователь user2 может отклонить предложение обмена.
    Статус предложения должен измениться на 'rejected'.
    """
    api_client.force_authenticate(user=user2)
    response = api_client.post(
        f'/api/proposals/{exchange_proposal.id}/reject/')
    exchange_proposal.refresh_from_db()

    assert response.status_code == 200
    assert exchange_proposal.status == ConstStr.REJECTED

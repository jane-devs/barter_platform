from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from ads.models import Ad

@pytest.mark.django_db
def test_ad_list_view(client):
    response = client.get(reverse('ad_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_ad_view(client):
    user = User.objects.create_user(username='testuser', password='pass')
    client.login(username='testuser', password='pass')
    response = client.post(reverse('ad_create'), {
        'title': 'Стол',
        'description': 'Деревянный',
        'category': 'furniture',
        'condition': 'used'
    })
    assert response.status_code == 302  # редирект после успешного создания
    assert Ad.objects.count() == 1

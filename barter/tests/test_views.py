import pytest
from django.urls import reverse
from django.utils.http import urlencode
from ads.models import Ad


@pytest.mark.django_db
def test_ad_list_view(client):
    """
    Проверка редиректа при попытке доступа к списку объявлений
    без аутентификации.
    """
    response = client.get(reverse('ad_list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_ad_view(client, user1):
    """
    Проверка создания объявления аутентифицированным пользователем.
    После успешного создания происходит редирект.
    """
    client.force_login(user1)
    response = client.post(reverse('ad_create'), {
        'title': 'Стол',
        'description': 'Деревянный',
        'category': 'furniture',
        'condition': 'used'
    })
    assert response.status_code == 302
    assert Ad.objects.filter(user=user1, title='Стол').exists()


@pytest.mark.django_db
def test_ad_list_view_authenticated(client, user1):
    """
    Проверка доступа к списку объявлений для аутентифицированного пользователя.
    В контексте должен присутствовать список объявлений.
    """
    client.force_login(user1)
    response = client.get(reverse('ad_list'))
    assert response.status_code == 200
    assert 'ads' in response.context


@pytest.mark.django_db
def test_ad_search_filter(client, user1):
    """
    Проверка фильтрации объявлений по поисковому запросу.
    Должно возвращаться только объявление, соответствующее поиску.
    """
    client.force_login(user1)
    Ad.objects.create(
        user=user1,
        title='Айфон',
        description='Устройство Apple',
        category='electronics',
        condition='new'
    )
    Ad.objects.create(
        user=user1,
        title='Самсунг',
        description='Телефон',
        category='electronics',
        condition='used'
    )
    url = reverse('ad_list') + '?' + urlencode({'search': 'Айфон'})
    response = client.get(url)
    assert response.status_code == 200
    ads = response.context['ads']
    assert ads.count() == 1
    assert 'Айфон' in ads[0].title


@pytest.mark.django_db
def test_ad_category_filter(client, user1):
    """
    Проверка фильтрации объявлений по категории.
    Возвращаются только объявления выбранной категории.
    """
    client.force_login(user1)
    Ad.objects.create(
        user=user1,
        title='Книга',
        description='Хорошая книга',
        category='books',
        condition='new'
    )
    Ad.objects.create(
        user=user1,
        title='Телефон',
        description='Старый телефон',
        category='electronics',
        condition='used'
    )
    url = reverse('ad_list') + '?' + urlencode({'category': 'books'})
    response = client.get(url)
    assert response.status_code == 200
    ads = response.context['ads']
    assert ads.count() == 1
    assert ads[0].category == 'books'


@pytest.mark.django_db
def test_ad_update_view(client, user1, ad1):
    """
    Проверка редактирования объявления его владельцем.
    После обновления данные должны сохраниться в базе.
    """
    client.force_login(user1)
    response = client.post(
        reverse('ad_update', args=[ad1.pk]),
        {
            'title': 'Новый заголовок',
            'description': 'Новое описание',
            'category': 'books',
            'condition': 'new',
        })

    assert response.status_code == 302
    ad1.refresh_from_db()
    assert ad1.title == 'Новый заголовок'
    assert ad1.condition == 'new'


@pytest.mark.django_db
def test_ad_update_view_no_permission(client, user2, ad1):
    """
    Проверка отказа в доступе при попытке редактировать чужое объявление.
    Возвращается статус 403 Forbidden.
    """
    client.force_login(user2)
    response = client.get(reverse('ad_update', args=[ad1.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_ad_delete_view(client, user1, ad1):
    """
    Проверка удаления объявления его владельцем.
    После удаления объявления его не должно быть в базе.
    """
    client.force_login(user1)
    response = client.post(reverse('ad_delete', args=[ad1.pk]))
    assert response.status_code == 302
    assert not Ad.objects.filter(pk=ad1.pk).exists()

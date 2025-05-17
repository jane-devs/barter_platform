import pytest
from ads.forms import AdForm, ExchangeProposalForm
from ads.models import Ad
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    """Фикстура для создания пользователя."""
    return User.objects.create_user(username='user1', password='pass')


@pytest.fixture
def ad(user):
    """Фикстура для создания объявления, принадлежащего пользователю."""
    return Ad.objects.create(
        user=user,
        title='Тестовое объявление',
        description='Описание',
        category='books',
        condition='new'
    )


@pytest.mark.django_db
def test_exchange_proposal_same_ads_form_validation_error(ad):
    """Проверка, что через форму нельзя отправить
    заявку за обмен одного и того же товара на самого себя.
    """
    form = ExchangeProposalForm(data={
        'ad_sender': ad.id,
        'comment': 'Обмен?'
    }, user=ad.user, ad_receiver=ad)

    assert not form.is_valid()
    assert '__all__' in form.errors
    assert (
        'Объявления отправителя и получателя не могут совпадать.'
    ) in form.errors['__all__']


@pytest.mark.django_db
def test_ad_form_valid_data():
    """
    Проверка валидности формы при корректных данных.
    Форма должна успешно проходить валидацию.
    """
    form = AdForm(data={
        'title': 'Корректный заголовок',
        'description': 'Корректное описание',
        'category': 'books',
        'condition': 'new',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_ad_form_missing_required():
    """
    Проверка ошибки валидации при отсутствии обязательного поля 'title'.
    Форма должна быть невалидной, ошибка должна быть у поля 'title'.
    """
    form = AdForm(data={
        'title': '',
        'description': 'Что-то',
        'category': 'books',
        'condition': 'new',
    })
    assert not form.is_valid()
    assert 'title' in form.errors


@pytest.mark.django_db
def test_ad_form_invalid_choice():
    """
    Проверка ошибки валидации при неверном выборе категории.
    Поле 'category' должно содержать ошибку.
    """
    form = AdForm(data={
        'title': 'Заголовок',
        'description': 'Описание',
        'category': 'invalid_cat',
        'condition': 'new',
    })
    assert not form.is_valid()
    assert 'category' in form.errors


@pytest.mark.django_db
def test_ad_form_edit_valid(ad):
    """
    Проверка редактирования объявления с корректными данными.
    После сохранения заголовок объявления должен измениться.
    """
    data = {
        'title': 'Изменённый заголовок',
        'description': ad.description,
        'category': ad.category,
        'condition': ad.condition,
        'image_url': ad.image_url or '',
    }
    form = AdForm(data=data, instance=ad)
    assert form.is_valid()
    updated_ad = form.save()
    assert updated_ad.title == 'Изменённый заголовок'


@pytest.mark.django_db
def test_ad_form_edit_invalid(ad):
    """
    Проверка редактирования объявления с некорректной категорией.
    Форма должна быть невалидной, ошибка должна быть у поля 'category'.
    """
    data = {
        'title': 'Заголовок',
        'description': ad.description,
        'category': 'wrong_cat',
        'condition': ad.condition,
        'image_url': ad.image_url or '',
    }
    form = AdForm(data=data, instance=ad)
    assert not form.is_valid()
    assert 'category' in form.errors


@pytest.mark.django_db
def test_ad_form_excludes_user_field():
    """
    Проверка, что поле 'user' отсутствует в форме.
    Пользователь задаётся автоматически, а не через форму.
    """
    form = AdForm()
    assert 'user' not in form.fields

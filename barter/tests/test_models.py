import pytest
from django.core.exceptions import ValidationError
from ads.models import Ad, ExchangeProposal
from constants import ConstStr


@pytest.mark.django_db
def test_ad_creation(user1):
    """
    Проверка успешного создания объявления с валидными данными.
    Убедиться, что объявление сохраняется и поля соответствуют ожидаемым.
    """
    ad = Ad.objects.create(
        user=user1,
        title='Телефон',
        description='Рабочий, немного поцарапан.',
        category='electronics',
        condition='used'
    )
    assert ad.pk is not None
    assert ad.title == 'Телефон'
    assert ad.condition == 'used'


@pytest.mark.django_db
def test_create_ad_with_missing_fields(user1):
    """
    Проверка ошибки валидации при создании объявления без обязательных полей.
    Метод full_clean должен вызвать ValidationError.
    """
    ad = Ad(user=user1)
    with pytest.raises(ValidationError):
        ad.full_clean()


@pytest.mark.django_db
def test_create_ad_with_invalid_condition(user1):
    """
    Проверка ошибки валидации при использовании
    недопустимого значения поля condition.
    """
    ad = Ad(
        user=user1,
        title='Тестовое объявление',
        description='Описание',
        category='electronics',
        condition='неизвестное_состояние'
    )
    with pytest.raises(ValidationError):
        ad.full_clean()


@pytest.mark.django_db
def test_exchange_proposal_with_invalid_status(user1):
    """
    Проверка ошибки валидации при установке
    недопустимого статуса у ExchangeProposal.
    """
    ad1 = Ad.objects.create(
        user=user1,
        title='Предмет 1',
        description='Что-то',
        category='books',
        condition='new'
    )
    ad2 = Ad.objects.create(
        user=user1,
        title='Предмет 2',
        description='Что-то другое',
        category='books',
        condition='used'
    )
    proposal = ExchangeProposal(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment='Поменяемся?',
        status='недопустимый_статус'
    )
    with pytest.raises(ValidationError):
        proposal.full_clean()


@pytest.mark.django_db
def test_edit_ad(ad1):
    """
    Проверка успешного редактирования объявления
    с изменением заголовка и описания.
    После сохранения изменения должны корректно сохраняться в базе данных.
    """
    ad1.title = 'Новый заголовок'
    ad1.description = 'Новое описание'
    ad1.full_clean()
    ad1.save()

    updated_ad = Ad.objects.get(pk=ad1.pk)
    assert updated_ad.title == 'Новый заголовок'
    assert updated_ad.description == 'Новое описание'


@pytest.mark.django_db
def test_edit_exchange_proposal(exchange_proposal):
    """
    Проверка редактирования ExchangeProposal: изменение комментария и статуса.
    Изменения должны сохраняться и корректно отражаться в базе данных.
    """
    exchange_proposal.comment = 'Отредактированный комментарий'
    exchange_proposal.status = ConstStr.ACCEPTED
    exchange_proposal.full_clean()
    exchange_proposal.save()

    updated_proposal = ExchangeProposal.objects.get(pk=exchange_proposal.pk)
    assert updated_proposal.comment == 'Отредактированный комментарий'
    assert updated_proposal.status == ConstStr.ACCEPTED


@pytest.mark.django_db
def test_delete_ad(ad1):
    """
    Проверка удаления объявления.
    После удаления попытка получить объявление
    по pk должна вызвать исключение DoesNotExist.
    """
    pk = ad1.pk
    ad1.delete()
    with pytest.raises(Ad.DoesNotExist):
        Ad.objects.get(pk=pk)


@pytest.mark.django_db
def test_delete_exchange_proposal(exchange_proposal):
    """
    Проверка удаления ExchangeProposal.
    После удаления попытка получить объект
    по pk должна вызвать исключение DoesNotExist.
    """
    pk = exchange_proposal.pk
    exchange_proposal.delete()
    with pytest.raises(ExchangeProposal.DoesNotExist):
        ExchangeProposal.objects.get(pk=pk)

import pytest
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_ad_creation():
    user = User.objects.create_user(username='testuser', password='pass1234')
    ad = Ad.objects.create(
        user=user,
        title='Телефон',
        description='Рабочий, немного поцарапан.',
        category='electronics',
        condition='used'
    )
    assert ad.pk is not None
    assert ad.title == 'Телефон'
    assert ad.condition == 'used'


@pytest.mark.django_db
def test_create_ad_with_missing_fields():
    user = User.objects.create_user(username="testuser", password="1234")
    ad = Ad(user=user)  # без title, description и т.д.

    with pytest.raises(ValidationError):
        ad.full_clean()


@pytest.mark.django_db
def test_create_ad_with_invalid_condition():
    user = User.objects.create_user(username="testuser2", password="1234")
    ad = Ad(
        user=user,
        title="Test Ad",
        description="Description",
        category="electronics",
        condition="nonexistent"  # Неверное значение
    )
    with pytest.raises(ValidationError):
        ad.full_clean()


@pytest.mark.django_db
def test_exchange_proposal_with_same_ads():
    user = User.objects.create_user(username="proposer", password="1234")
    ad = Ad.objects.create(
        user=user,
        title="Phone",
        description="Smartphone",
        category="electronics",
        condition="used"
    )
    proposal = ExchangeProposal(
        ad_sender=ad,
        ad_receiver=ad,
        comment="Let's trade"
    )
    proposal.full_clean()
    proposal.save()

    assert proposal.ad_sender == proposal.ad_receiver


@pytest.mark.django_db
def test_exchange_proposal_with_invalid_status():
    user = User.objects.create_user(username="invalidstatus", password="1234")
    ad1 = Ad.objects.create(
        user=user,
        title="Item 1",
        description="Something",
        category="books",
        condition="new"
    )
    ad2 = Ad.objects.create(
        user=user,
        title="Item 2",
        description="Something else",
        category="books",
        condition="used"
    )

    proposal = ExchangeProposal(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment="Please exchange",
        status="invalid_status"
    )

    with pytest.raises(ValidationError):
        proposal.full_clean()

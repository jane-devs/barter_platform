import pytest
from ads.forms import AdForm


@pytest.mark.django_db
def test_ad_form_valid_data():
    form = AdForm(data={
        'title': 'Valid title',
        'description': 'Valid desc',
        'category': 'books',
        'condition': 'new',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_ad_form_missing_required():
    form = AdForm(data={
        'title': '',  # пустое поле
        'description': 'Something',
        'category': 'books',
        'condition': 'new',
    })
    assert not form.is_valid()
    assert 'title' in form.errors


@pytest.mark.django_db
def test_ad_form_invalid_choice():
    form = AdForm(data={
        'title': 'Title',
        'description': 'Desc',
        'category': 'invalid_cat',
        'condition': 'new',
    })
    assert not form.is_valid()
    assert 'category' in form.errors

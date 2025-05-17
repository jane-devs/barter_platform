from django import forms
from django.core.exceptions import ValidationError

from .models import Ad, ExchangeProposal
from constants import ConstStr, ConstNum


class AdForm(forms.ModelForm):
    """
    Форма для создания и редактирования объявления.
    """

    class Meta:
        model = Ad
        exclude = ['user']
        fields = [
            ConstStr.TITLE,
            ConstStr.DESCRIPTION,
            ConstStr.IMAGE_URL,
            ConstStr.CATEGORY,
            ConstStr.CONDITION
        ]
        widgets = {
            ConstStr.TITLE: forms.TextInput(
                attrs={'class': 'form-control'}),
            ConstStr.DESCRIPTION: forms.Textarea(
                attrs={'class': 'form-control', 'rows': ConstNum.DESC_ROWS}),
            ConstStr.CATEGORY: forms.Select(
                attrs={'class': 'form-select'}),
            ConstStr.CONDITION: forms.Select(
                attrs={'class': 'form-select'}),
            ConstStr.IMAGE_URL: forms.URLInput(
                attrs={'class': 'form-control'}),
        }


class ExchangeProposalForm(forms.ModelForm):
    """
    Форма для отправки предложения обмена.
    """

    class Meta:
        model = ExchangeProposal
        fields = [ConstStr.AD_SENDER, ConstStr.COMMENT]
        widgets = {
            ConstStr.AD_SENDER: forms.Select(
                attrs={'class': 'form-select'}),
            ConstStr.COMMENT: forms.Textarea(
                attrs={'class': 'form-control',
                       'rows': ConstNum.COMMENTS_ROWS}),
        }

    def __init__(self, *args, user=None, ad_receiver=None, **kwargs):
        """
        Фильтрует список объявлений пользователя, исключая уже обменянные,
        и сохраняет переданное объявление получателя.
        """

        super().__init__(*args, **kwargs)
        if user:
            self.fields[ConstStr.AD_SENDER].queryset = Ad.objects.filter(
                user=user,
                is_exchanged=False
            )
        if ad_receiver:
            self.ad_receiver = ad_receiver

    def clean(self):
        cleaned_data = super().clean()
        ad_sender = cleaned_data.get('ad_sender')

        if ad_sender == self.ad_receiver:
            raise ValidationError(
                "Объявления отправителя и получателя не могут совпадать.",
                code='invalid'
            )
        return cleaned_data

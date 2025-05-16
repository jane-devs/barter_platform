from django import forms
from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    image_url = forms.URLField(required=False, assume_scheme='https')

    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'condition': forms.Select(choices=Ad.CONDITION_CHOICES),
        }


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

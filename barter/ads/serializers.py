from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'user')


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'status')
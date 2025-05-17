from django.contrib.auth.models import User
from rest_framework import serializers

from ads.models import Ad, ExchangeProposal


class UserShortSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор для Ad для отображения
    пользователя.
    """
    class Meta:
        model = User
        fields = ['id', 'username']


class AdSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ad.
    Используется для отображения объявлений.
    """
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description', 'category',
            'image_url', 'condition', 'is_exchanged', 'created_at', 'user'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AdCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ad.
    Используется для создания объявлений.
    Исключены user и дата создания.
    """
    class Meta:
        model = Ad
        exclude = ['user', 'created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ExchangeProposal.
    Представляет предложения на обмен между пользователями.
    """
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver',
            'status', 'created_at', 'user'
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя Django.
    Используется для базового отображения информации о пользователе.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

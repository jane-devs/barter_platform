from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from ads.models import Ad, ExchangeProposal
from .serializers import (
    AdSerializer, ExchangeProposalSerializer, UserSerializer,
    AdCreateSerializer, EmptySerializer
)
from .mixins import AdsFilterMixin, IsOwnerPermission
from constants import ConstStr, Errors, Message
from services.proposal_service import (
    process_proposal_action, create_exchange_proposal,
    ProposalCreationError
)
from services.registration import register_user, RegistrationError


class AdViewSet(AdsFilterMixin, viewsets.ModelViewSet):
    """
    API эндпоинты для работы с объявлениями.

    Реализует GET списка, POST, GET одного объявления,
    PUT, PATCH и DELETE методы.
    """

    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [ConstStr.TITLE, ConstStr.DESCRIPTION]
    filterset_fields = [ConstStr.CATEGORY, ConstStr.CONDITION]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_ads_queryset(queryset).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return AdSerializer
        return AdCreateSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Поиск по заголовку и описанию',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                description='Фильтр по категории',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='condition',
                in_=openapi.IN_QUERY,
                description='Фильтр по состоянию',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description=(
                    'Сортировка: title, -title, created_at, -created_at'
                ),
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    """
    API эндпоинты для предложений обмена.

    Реализует GET списка предложений, POST,
    GET одного предложения,
    PUT, PATCH и DELETE методы. Также два POST-метода
    для принятия или отклонения предложения обмена.
    """

    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'status',
        'ad_sender__user__username',
        'ad_receiver__user__username'
    ]

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        )

    def perform_create(self, serializer):
        ad_sender = serializer.validated_data.get('ad_sender')
        if ad_sender.user != self.request.user:
            raise serializers.ValidationError(Errors.ONLY_YOUR_PROPOSAL)

        try:
            create_exchange_proposal(
                user=self.request.user,
                ad_receiver_id=serializer.validated_data['ad_receiver'].id,
                ad_sender=ad_sender
            )
        except ProposalCreationError as e:
            raise serializers.ValidationError(str(e))

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='status',
                in_=openapi.IN_QUERY,
                description=(
                    'Фильтрация по статусу предложения: '
                    '(pending, accepted, rejected)'
                ),
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='ad_sender',
                in_=openapi.IN_QUERY,
                description='Фильтрация: имя пользователя отправителя',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='ad_receiver',
                in_=openapi.IN_QUERY,
                description='Фильтрация: имя пользователя получателя',
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(request_body=EmptySerializer)
    @action(
        detail=True,
        methods=['post'],
        serializer_class=EmptySerializer
    )
    def accept(self, request, pk=None):
        """
        Принять предложение обмена.

        POST-запрос для принятия предложения обмена.
        Тело запроса не передается (в документации отображается как {}).

        Для принятия предложения просто укажите id предложения.
        """
        return self._handle_proposal_action(request, pk, 'accept')

    @swagger_auto_schema(request_body=EmptySerializer)
    @action(
        detail=True,
        methods=['post'],
        serializer_class=EmptySerializer
    )
    def reject(self, request, pk=None):
        """
        Отклонить предложение обмена.

        POST-запрос для отказа на предложение обмена.
        Тело запроса не передается (в документации отображается как {}).

        Для отклонения предложения просто укажите id предложения.
        """
        return self._handle_proposal_action(request, pk, 'reject')

    def _handle_proposal_action(self, request, pk, action):
        proposal = self.get_object()
        result = process_proposal_action(proposal, action, request.user)
        if result['error']:
            raise ValidationError(result['message'])
        return Response({'status': result['message']})


class UserViewSet(viewsets.ViewSet):
    """
    API эндпоинты для пользователей.

    ViewSet для получения текущего пользователя и регистрации.
    """

    @swagger_auto_schema(
        method='get',
        responses={200: UserSerializer()},
        operation_description='Получить текущего авторизованного пользователя'
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Получение информации о текущем пользователе."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: openapi.Response('Регистрация успешна')},
        operation_description='Зарегистрировать нового пользователя'
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация пользователя."""
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            register_user(request, username, password)
        except RegistrationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'detail': Message.REGISTRATION_SUCCESS},
            status=status.HTTP_201_CREATED
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный токен для русификации документации."""
    @swagger_auto_schema(
        operation_summary='Получить JWT токены',
        operation_description=(
            'Получает пару токенов (access и refresh) по логину и паролю.'
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING, description='Имя пользователя'),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, description='Пароль'),
            },
        ),
        responses={200: openapi.Response(
            description='Успешная авторизация. Возвращает токены.')},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    """Кастомный рефреш-токен для русификации документации."""
    @swagger_auto_schema(
        operation_summary='Обновить JWT токен',
        operation_description=(
            'Принимает refresh-токен и возвращает новый access-токен.'
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING, description='Refresh-токен'),
            },
        ),
        responses={200: openapi.Response(description='Новый access токен')},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

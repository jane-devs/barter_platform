from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import AdsFilterMixin, IsOwnerPermission


class AdViewSet(AdsFilterMixin, viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]  # проверка владения
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'condition']

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_ads_queryset(queryset).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            ad_sender__user=user
        ) | ExchangeProposal.objects.filter(
            ad_receiver__user=user
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        if proposal.status != 'pending':
            return Response({"detail": "Предложение уже обработано."}, status=status.HTTP_400_BAD_REQUEST)
        if proposal.ad_receiver.user != request.user:
            return Response({"detail": "Нет прав."}, status=status.HTTP_403_FORBIDDEN)

        proposal.status = 'accepted'
        proposal.ad_sender.is_exchanged = True
        proposal.ad_receiver.is_exchanged = True
        proposal.ad_sender.save()
        proposal.ad_receiver.save()
        proposal.save()
        return Response({"detail": "Предложение принято."})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        proposal = self.get_object()
        if proposal.status != 'pending':
            return Response({"detail": "Предложение уже обработано."}, status=status.HTTP_400_BAD_REQUEST)
        if proposal.ad_receiver.user != request.user:
            return Response({"detail": "Нет прав."}, status=status.HTTP_403_FORBIDDEN)

        proposal.status = 'rejected'
        proposal.save()
        return Response({"detail": "Предложение отклонено."})
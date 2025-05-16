from rest_framework import viewsets, permissions, filters
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AdForm, ExchangeProposalForm


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return super().get_permissions()


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False)
    def filter(self, request):
        sender = request.query_params.get('ad_sender')
        receiver = request.query_params.get('ad_receiver')
        status = request.query_params.get('status')
        proposals = self.queryset

        if sender:
            proposals = proposals.filter(ad_sender__id=sender)
        if receiver:
            proposals = proposals.filter(ad_receiver__id=receiver)
        if status:
            proposals = proposals.filter(status=status)

        page = self.paginate_queryset(proposals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(proposals, many=True)
        return Response(serializer.data)


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def update_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ad_list.html', {'ads': ads})


@login_required
def create_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads/proposal_form.html', {'form': form})


def redirect_to_ads(request):
    return redirect('ad_list')
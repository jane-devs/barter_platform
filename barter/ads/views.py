from django.views.generic import CreateView, UpdateView, DeleteView, ListView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.db.models import Q
from .mixins import AdsFilterMixin, IsOwnerMixin


class AdListView(LoginRequiredMixin, AdsFilterMixin, ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_ads_queryset(queryset).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ads = Ad.objects.filter(user=self.request.user)
        context['proposed_ads_ids'] = set(
            ExchangeProposal.objects.filter(ad_sender__in=user_ads, status='pending')
            .values_list('ad_receiver_id', flat=True)
        )
        context['exchanged_ads_ids'] = set(
            Ad.objects.filter(is_exchanged=True).values_list('id', flat=True)
        )
        context['search_query'] = self.get_search_param()
        context['filter_category'] = self.get_category_param()
        context['filter_condition'] = self.get_condition_param()
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, IsOwnerMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.is_owner(ad)


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, IsOwnerMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.is_owner(ad)


class ProposalCreateView(LoginRequiredMixin, FormView):
    template_name = 'ads/proposal_form.html'
    form_class = ExchangeProposalForm
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        self.ad_receiver = get_object_or_404(Ad, pk=self.kwargs['ad_pk'], is_exchanged=False)
        if self.ad_receiver.user == request.user:
            messages.error(request, "Вы не можете предлагать обмен самому себе.")
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['ad_receiver'] = self.ad_receiver
        return kwargs

    def form_valid(self, form):
        proposal = form.save(commit=False)
        proposal.ad_receiver = self.ad_receiver
        proposal.status = 'pending'
        proposal.save()
        messages.success(self.request, "Предложение обмена отправлено.")
        return super().form_valid(form)


class MyProposalsView(LoginRequiredMixin, View):
    def get(self, request):
        user_ads = Ad.objects.filter(user=request.user)
        sent_proposals = ExchangeProposal.objects.filter(ad_sender__in=user_ads)
        received_proposals = ExchangeProposal.objects.filter(ad_receiver__in=user_ads)
        return render(request, 'ads/my_proposals.html', {
            'sent_proposals': sent_proposals,
            'received_proposals': received_proposals,
        })


class HandleProposalView(LoginRequiredMixin, View):
    def post(self, request, proposal_id, action):
        proposal = get_object_or_404(ExchangeProposal, pk=proposal_id, ad_receiver__user=request.user)

        if proposal.status != 'pending':
            messages.info(request, "Это предложение уже обработано.")
            return redirect('my_proposals')

        if action == 'accept':
            proposal.status = 'accepted'
            proposal.ad_sender.is_exchanged = True
            proposal.ad_receiver.is_exchanged = True
            proposal.ad_sender.save()
            proposal.ad_receiver.save()
            messages.success(request, "Вы приняли предложение обмена.")
        elif action == 'reject':
            proposal.status = 'rejected'
            messages.success(request, "Вы отклонили предложение обмена.")
        else:
            return HttpResponseBadRequest("Неверное действие.")
        
        proposal.save()
        return redirect('my_proposals')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, FormView, View,
    TemplateView
)

from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from api.mixins import AdsFilterMixin, IsOwnerMixin
from constants import ConstStr, ConstNum, Message, Errors
from services.proposal_service import (
    process_proposal_action, create_exchange_proposal,
    ProposalCreationError
)
from services.registration import register_user, RegistrationError


class AdListView(LoginRequiredMixin, AdsFilterMixin, ListView):
    """
    Представление для отображения списка объявлений
    с фильтрацией, сортировкой и пагинацией.
    """

    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = ConstNum.PAGINATION_COUNT
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_ads_queryset(queryset)
        if self.request.GET.get(
            'my_ads'
        ) and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        order_by = self.request.GET.get('order_by')
        if order_by in [
            ConstStr.TITLE,
            f'-{ConstStr.TITLE}',
            '-created_at'.lstrip('-'),
            '-created_at',
        ]:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ads = Ad.objects.filter(user=self.request.user)
        context['proposed_ads_ids'] = set(
            ExchangeProposal.objects.filter(
                ad_sender__in=user_ads,
                status=ConstStr.PENDING
            ).values_list('ad_receiver_id', flat=True)
        )
        context['exchanged_ads_ids'] = set(
            Ad.objects.filter(is_exchanged=True).values_list('id', flat=True)
        )
        context['search_query'] = self.get_search_param()
        context['filter_category'] = self.get_category_param()
        context['filter_condition'] = self.get_condition_param()
        context['category_choices'] = Ad._meta.get_field(
            ConstStr.CATEGORY).choices
        context['condition_choices'] = Ad._meta.get_field(
            ConstStr.CONDITION).choices
        context['my_ads_checked'] = bool(self.request.GET.get('my_ads'))
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    """Создание нового объявления текущим пользователем."""

    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    IsOwnerMixin,
    UpdateView
):
    """Редактирование объявления, доступно только владельцу."""

    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.is_owner(ad)


class AdDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    IsOwnerMixin,
    DeleteView
):
    """Удаление объявления, доступно только владельцу."""

    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.is_owner(ad)


class ProposalCreateView(LoginRequiredMixin, FormView):
    """
    Создание предложения обмена текущим
    пользователем для чужого объявления.
    """

    template_name = 'ads/proposal_form.html'
    form_class = ExchangeProposalForm
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        self.ad_receiver = get_object_or_404(
            Ad, pk=self.kwargs['ad_pk'], is_exchanged=False
        )
        if self.ad_receiver.user == request.user:
            messages.error(request, Errors.ERROR_SELF_PROPOSAL)
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['ad_receiver'] = self.ad_receiver
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = self.ad_receiver
        return context

    def form_valid(self, form):
        try:
            create_exchange_proposal(
                user=self.request.user,
                ad_receiver_id=self.ad_receiver.id,
                ad_sender=form.cleaned_data['ad_sender']
            )
        except ProposalCreationError as e:
            messages.error(self.request, str(e))
            return redirect('ad_list')

        messages.success(self.request, Message.SUCCESS_PROPOSAL_SENT)
        return super().form_valid(form)


class MyProposalsView(LoginRequiredMixin, TemplateView):
    """
    Отображение предложений, отправленных
    и полученных текущим пользователем, с фильтрацией.
    """

    template_name = 'ads/my_proposals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_ads = Ad.objects.filter(user=user)
        sent_proposals = ExchangeProposal.objects.filter(
            ad_sender__in=user_ads)
        received_proposals = ExchangeProposal.objects.filter(
            ad_receiver__in=user_ads)
        status_filter = self.request.GET.get('status')
        sender_filter = self.request.GET.get('sender', '').strip()
        receiver_filter = self.request.GET.get('receiver', '').strip()
        if status_filter in [
            ConstStr.PENDING,
            ConstStr.ACCEPTED,
            ConstStr.REJECTED
        ]:
            sent_proposals = sent_proposals.filter(
                status=status_filter)
            received_proposals = received_proposals.filter(
                status=status_filter)
        if sender_filter:
            received_proposals = received_proposals.filter(
                ad_sender__user__username__icontains=sender_filter
            )
        if receiver_filter:
            sent_proposals = sent_proposals.filter(
                ad_receiver__user__username__icontains=receiver_filter
            )
        sent_page_number = self.request.GET.get('sent_page')
        sent_paginator = Paginator(sent_proposals, 5)
        sent_page_obj = sent_paginator.get_page(sent_page_number)
        received_page_number = self.request.GET.get('received_page')
        received_paginator = Paginator(received_proposals, 5)
        received_page_obj = received_paginator.get_page(received_page_number)
        base_query = {}
        if status_filter:
            base_query['status'] = status_filter
        if sender_filter:
            base_query['sender'] = sender_filter
        if receiver_filter:
            base_query['receiver'] = receiver_filter
        query_string = urlencode(base_query)
        context.update({
            'sent_page_obj': sent_page_obj,
            'received_page_obj': received_page_obj,
            'sent_proposals': sent_page_obj.object_list,
            'received_proposals': received_page_obj.object_list,
            'status_filter': status_filter,
            'sender_filter': sender_filter,
            'receiver_filter': receiver_filter,
            'query_string': query_string,
        })
        return context


class HandleProposalView(LoginRequiredMixin, View):
    """Обработка ответа на предложения обмена."""

    def post(self, request, proposal_id: int, action: str):
        proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)
        result = process_proposal_action(proposal, action, request.user)
        if result['error']:
            messages.error(request, result['message'])
        else:
            messages.success(request, result['message'])
        return redirect('my_proposals')


class RegisterView(FormView):
    """
    Регистрация нового пользователя
    с автоматическим входом в систему.
    """
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        try:
            register_user(self.request, username, password)
        except RegistrationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        return super().form_valid(form)

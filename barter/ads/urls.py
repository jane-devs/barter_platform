from .views import (
    AdListView, AdCreateView, AdUpdateView, AdDeleteView,
    ProposalCreateView, MyProposalsView, HandleProposalView, RegisterView
)
from django.urls import path



urlpatterns = [
    path('ads/', AdListView.as_view(), name='ad_list'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    path('accounts/register/', RegisterView.as_view(), name='register'),

    path('proposals/create/<int:ad_pk>/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/', MyProposalsView.as_view(), name='my_proposals'),
    path('proposals/<int:proposal_id>/<str:action>/', HandleProposalView.as_view(), name='handle_proposal'),
]

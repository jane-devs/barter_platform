from django.urls import path

from .views import (
    AdCreateView,
    AdDeleteView,
    AdListView,
    AdUpdateView,
    HandleProposalView,
    MyProposalsView,
    ProposalCreateView,
    RegisterView
)

urlpatterns = [
    path('ads/', AdListView.as_view(), name='ad_list'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('proposals/', MyProposalsView.as_view(), name='my_proposals'),
    path(
        'proposals/create/<int:ad_pk>/',
        ProposalCreateView.as_view(),
        name='proposal_create'
    ),
    path(
        'proposals/<int:proposal_id>/<str:action>/',
        HandleProposalView.as_view(),
        name='handle_proposal'
    ),
    path('accounts/register/', RegisterView.as_view(), name='register'),
]

from django.core.exceptions import PermissionDenied
from ads.models import ExchangeProposal


def check_proposal_access(proposal: ExchangeProposal, user):
    if proposal.ad_receiver.user != user:
        raise PermissionDenied('Недостаточно прав для выполнения действия.')

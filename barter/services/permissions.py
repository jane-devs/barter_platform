from django.core.exceptions import PermissionDenied

from ads.models import ExchangeProposal
from constants import Errors


def check_proposal_access(proposal: ExchangeProposal, user):
    if proposal.ad_receiver.user != user:
        raise PermissionDenied(Errors.NO_PERMISSION)

from django.core.exceptions import PermissionDenied
from ads.models import ExchangeProposal, StatusChoices
from django.db import transaction


class ProposalAlreadyHandledError(Exception):
    pass


@transaction.atomic
def handle_proposal_action(proposal: ExchangeProposal, action: str, user):
    if proposal.status != StatusChoices.PENDING:
        raise ProposalAlreadyHandledError("Proposal already handled.")

    if proposal.ad_receiver.user != user:
        raise PermissionDenied("You are not allowed to handle this proposal.")

    if action == 'accept':
        proposal.status = StatusChoices.ACCEPTED
        proposal.ad_sender.is_exchanged = True
        proposal.ad_receiver.is_exchanged = True
        proposal.ad_sender.save()
        proposal.ad_receiver.save()

    elif action == 'reject':
        proposal.status = StatusChoices.REJECTED
    else:
        raise ValueError('Unknown action')

    proposal.save()

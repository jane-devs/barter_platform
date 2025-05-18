from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404

from ads.models import ExchangeProposal, StatusChoices, Ad
from constants import Message, Errors, ConstStr
from .messages import get_proposal_action_message


class ProposalAlreadyHandledError(Exception):
    """Кастомное исключение для предложений обмена."""
    pass


@transaction.atomic
def handle_proposal_action(proposal: ExchangeProposal, action: str, user):
    """Бизнес-логика предложений обмена."""
    if proposal.status != StatusChoices.PENDING:
        raise ProposalAlreadyHandledError(Message.PROPOSAL_ALREADY)
    if proposal.ad_receiver.user != user:
        raise PermissionDenied(Errors.ERROR_PROPOSAL)
    if action == 'accept':
        proposal.status = StatusChoices.ACCEPTED
        proposal.ad_sender.is_exchanged = True
        proposal.ad_receiver.is_exchanged = True
        proposal.ad_sender.save()
        proposal.ad_receiver.save()
    elif action == 'reject':
        proposal.status = StatusChoices.REJECTED
    else:
        raise ValueError(Message.UNKNOWN_ACTION)
    proposal.save()


def process_proposal_action(proposal, action, user):
    """
    Вызывает бизнес-логику обработки предложения,
    возвращает dict с результатом и сообщением.
    """
    try:
        handle_proposal_action(proposal, action, user)
    except ProposalAlreadyHandledError:
        return {
            'error': True,
            'message': get_proposal_action_message('already_handled')
        }
    except PermissionDenied:
        return {
            'error': True,
            'message': get_proposal_action_message('forbidden')
        }
    except ValueError:
        return {
            'error': True,
            'message': get_proposal_action_message('invalid_action')
        }
    else:
        return {
            'error': False,
            'message': get_proposal_action_message('success', action)
        }


class ProposalCreationError(Exception):
    """Кастомное исключение создания предложения обмена."""
    pass


def create_exchange_proposal(user, ad_receiver_id, ad_sender):
    """Сервисная функция для создания предложения обмена."""
    ad_receiver = get_object_or_404(Ad, pk=ad_receiver_id, is_exchanged=False)

    if ad_receiver.user == user:
        raise ProposalCreationError(Errors.ERROR_SELF_PROPOSAL)

    proposal = ExchangeProposal(
        ad_receiver=ad_receiver,
        ad_sender=ad_sender,
        status=ConstStr.PENDING
    )
    proposal.save()
    return proposal

from constants import Message, Errors, ConstStr


def get_proposal_action_message(code: str, action: str = None) -> str:
    """Обработка ответа на предложение."""
    action_labels = {
        'accept': ConstStr.ACCEPTED_RU,
        'reject': ConstStr.REJECTED_RU,
    }
    messages = {
        'success': Message.GET_PROPOSAL.format(
            get_action=action_labels.get(action, ConstStr.PROCESSED)),
        'already_handled': Message.PROPOSAL_ALREADY,
        'forbidden': Errors.ERROR_PROPOSAL,
        'invalid_action': Message.UNKNOWN_ACTION,
    }
    return messages.get(code, Errors.UNKNOWN_RESULT)

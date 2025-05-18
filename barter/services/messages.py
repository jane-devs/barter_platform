def get_proposal_action_message(code: str, action: str = None) -> str:
    action_labels = {
        'accept': 'приняли',
        'reject': 'отклонили',
    }
    messages = {
        'success': f'Вы успешно {action_labels.get(action, "обработали")} '
                   f'предложение.',
        'already_handled': 'Предложение уже обработано.',
        'forbidden': 'Вы не можете обработать это предложение.',
        'invalid_action': 'Недопустимое действие.',
    }
    return messages.get(code, 'Неизвестный результат.')

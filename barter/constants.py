class Message:
    PROPOSAL_ALREADY = 'Предложение уже обработано.'
    PROPOSAL_ACCEPT = 'Предложение принято.'
    PROPOSAL_REJECT = 'Предложение отклонено.'
    SUCCESS_PROPOSAL_SENT = 'Предложение обмена отправлено.'
    REG_DATA_REQUIRED = 'Необходимы юзернейм и пароль.'
    REGISTRATION_SUCCESS = 'Успешная регистрация.'
    UNKNOWN_ACTION = 'Неизвестное действие'
    GET_PROPOSAL = 'Вы успешно {get_action} предложение.'


class Errors:
    NO_PERMISSION = 'Недостаточно прав для выполнения действия.'
    ERROR_SELF_PROPOSAL = 'Вы не можете предлагать обмен самому себе.'
    ERROR_PROPOSAL = 'Вы не можете предлагать этот обмен.'
    WRONG_ACTION = 'Некорректное действие.'
    ONLY_YOUR_PROPOSAL = (
        'Вы можете предлагать только свои объявления на обмен.')
    USERNAME_TAKEN = 'Юзернейм уже занят!'
    UNKNOWN_RESULT = 'Неизвестный результат.'
    SAME_PROPOSAL = 'Объявления отправителя и получателя не могут совпадать.'


class ConstNum:
    COMMENTS_ROWS = 3
    DESC_ROWS = 4
    PAGINATION_COUNT = 10


class ConstStr:
    TITLE = 'title'
    DESCRIPTION = 'description'
    CATEGORY = 'category'
    CONDITION = 'condition'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    ACCEPTED_RU = 'приняли'
    REJECTED = 'rejected'
    REJECTED_RU = 'отклонили'
    PROCESSED = 'обработали'
    DETAIL = 'detail'
    IMAGE_URL = 'image_url'
    AD_SENDER = 'ad_sender'
    COMMENT = 'comment'

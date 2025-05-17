class Message:
    PROPOSAL_ALREADY = 'Предложение уже обработано.'
    PROPOSAL_ACCEPT = 'Предложение принято.'
    PROPOSAL_REJECT = 'Предложение отклонено.'


class Errors:
    NO_PERMISSION = 'Нет прав.'


class ConstNum:
    COMMENTS_ROWS = 3
    DESC_ROWS = 4
    PAGINATION_COUNT = 10


class ConstStr:
    TITLE = 'title'
    DESCRIPTION = 'description'
    CATEGORY = 'category'
    CONDITION = 'condition'
    POST = 'post'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DETAIL = 'detail'
    IMAGE_URL = 'image_url'
    AD_SENDER = 'ad_sender'
    COMMENT = 'comment'
    ERROR_SELF_PROPOSAL = 'Вы не можете предлагать обмен самому себе.'
    SUCCESS_PROPOSAL_SENT = 'Предложение обмена отправлено.'
    WRONG_ACTION = 'Некорректное действие.'
    ONLY_YOUR_PROPOSAL = (
        'Вы можете предлагать только свои объявления на обмен.')
    REG_DATA_REQUIRED = 'Необходимы юзернейм и пароль.'
    USERNAME_TAKEN = 'Юзернейм уже занят!'
    REGISTRATION_SUCCESS = 'Успешная регистрация.'

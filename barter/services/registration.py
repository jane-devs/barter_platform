from django.contrib.auth import get_user_model, login
from constants import Message, Errors

User = get_user_model()


class RegistrationError(Exception):
    """Кастомное исключение для ошибок регистрации"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def register_user(
    request,
    username: str,
    password: str
):
    """Сервисная функция для регистрации пользователя."""
    if not username or not password:
        raise RegistrationError(Message.REG_DATA_REQUIRED)
    if User.objects.filter(username=username).exists():
        raise RegistrationError(Errors.USERNAME_TAKEN)
    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return user

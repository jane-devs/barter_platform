from django.shortcuts import render
from rest_framework import status


def handler400(request, exception):
    """Обработчик ошибки 400 — некорректный запрос."""
    return render(
        request, 'errors/400.html', status=status.HTTP_400_BAD_REQUEST)


def handler403(request, exception):
    """Обработчик ошибки 403 — запрет доступа."""
    return render(
        request, 'errors/403.html', status=status.HTTP_403_FORBIDDEN)


def handler404(request, exception):
    """Обработчик ошибки 404 — страница не найдена."""
    return render(
        request, 'errors/404.html', status=status.HTTP_404_NOT_FOUND)


def handler500(request):
    """Обработчик ошибки 500 — ошибка сервера."""
    return render(
        request,
        'errors/500.html',
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

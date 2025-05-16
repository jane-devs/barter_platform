from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        abstract = True


class Ad(BaseModel):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
    ]
    CATEGORY_CHOICES = [
        ('books', 'Книги'),
        ('electronics', 'Электроника'),
        ('clothes', 'Одежда'),
        ('furniture', 'Мебель'),
        ('toys', 'Игрушки'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ads', verbose_name='Создатель')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание товара')
    image_url = models.URLField(blank=True, null=True, verbose_name='Фото товара')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name='Состояние')
    is_exchanged = models.BooleanField(default=False, verbose_name='Обмен завершён')

    def __str__(self):
        return self.title


class ExchangeProposal(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals', verbose_name='Ваш товар на обмен')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус обмена')

    def __str__(self):
        return f"Предложение от {self.ad_sender} к {self.ad_receiver}"

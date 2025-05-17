from django.contrib.auth.models import User
from django.db import models


class CategoryChoices(models.TextChoices):
    BOOKS = 'books', 'Книги'
    ELECTRONICS = 'electronics', 'Электроника'
    CLOTHES = 'clothes', 'Одежда'
    FURNITURE = 'furniture', 'Мебель'
    TOYS = 'toys', 'Игрушки'
    OTHER = 'other', 'Другое'


class ConditionChoices(models.TextChoices):
    NEW = 'new', 'Новый'
    USED = 'used', 'Б/у'


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    ACCEPTED = 'accepted', 'Принята'
    REJECTED = 'rejected', 'Отклонена'


class BaseModel(models.Model):
    """
    Абстрактная базовая модель с полем даты создания.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    class Meta:
        abstract = True


class Ad(BaseModel):
    """
    Модель объявления о товаре, доступном для обмена.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Создатель'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Фото товара'
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        verbose_name='Категория'
    )
    condition = models.CharField(
        max_length=10,
        choices=ConditionChoices.choices,
        verbose_name='Состояние'
    )
    is_exchanged = models.BooleanField(
        default=False,
        verbose_name='Состояние обмена'
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ExchangeProposal(BaseModel):
    """
    Модель предложения обмена между двумя объявлениями.
    """

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name='Ваш товар на обмен'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name='Получаемый товар'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default='pending',
        verbose_name='Статус обмена'
    )

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        ordering = ['-created_at']

    def __str__(self):
        return f'Обмен от {self.ad_sender} к {self.ad_receiver}'

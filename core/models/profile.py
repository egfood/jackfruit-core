from django.conf import settings
from django.db import models

from apps import store
from .base import FoodAbstract


class UserProfile(FoodAbstract):
    office = models.ForeignKey("store.OfficeLocation", verbose_name="Офис",
                              related_name='user_profile', on_delete=models.SET_NULL, blank=True, null=True)

    phone = models.CharField(verbose_name="Телефон", max_length=15, blank=True)
    notes = models.TextField(verbose_name="Примечания к пользователю", blank=True)
    tg_username = models.CharField(verbose_name='Username в телеграмме', max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', related_name='user_profile',
                             on_delete=models.CASCADE)

    USER_ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('supplier', 'Поставщик'),
    )
    DEFAULT_USER_ROLE = USER_ROLE_CHOICES[0][0]
    user_role = models.CharField(verbose_name="Роль пользователя", max_length=20, choices=USER_ROLE_CHOICES,
                                 default=DEFAULT_USER_ROLE)

    def __str__(self):
        return f'Профиль пользователя {self.user}'

    @property
    def is_buyer(self):
        return self.user_role == 'buyer'

    @property
    def is_supplier(self):
        return self.user_role == 'supplier'

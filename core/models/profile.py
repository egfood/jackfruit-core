from django.conf import settings
from django.db import models

from .base import FoodAbstract


class AbsProfile(FoodAbstract):
    _profile_type = None

    class Meta:
        abstract = True

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                related_name='%(app_label)_%(class)',
                                on_delete=models.CASCADE)
    photo = models.ImageField('Фото', upload_to='profile_photos', max_length=255, blank=True)

    @property
    def type(self):
        if self._profile_type is None:
            self._profile_type = self.__class__.__name__
        return self._profile_type

    def __str__(self):
        return f'Профиль пользователя {self.user}[{self.type}]'
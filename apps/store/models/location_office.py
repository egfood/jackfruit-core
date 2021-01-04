from django.conf import settings
from django.db import models

from .location import LocationAbstract


class OfficeLocation(LocationAbstract):
    SHORT_NAME_CHOICES = settings.OFFICES_SHORT_NAME_CHOICES

    short_name = models.TextField("Короткое название", max_length=settings.OFFICES_SHORT_NAME_LENGTH,
                                  default=settings.DEFAULT_OFFICE, unique=True)

    def __str__(self):
        return self.short_name

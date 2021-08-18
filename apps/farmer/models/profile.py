from django.db import models

from core.models import AbsProfile


class FarmerProfile(AbsProfile):
    service_zone = models.TextField(verbose_name='Зона обслуживания', blank=True, default="")
    legal_name = models.CharField(verbose_name='Название компании / фермерского хозяйства', max_length=500, blank=True,
                                  default="")

    @property
    def stringify_profile_type(self):
        return "фермера"

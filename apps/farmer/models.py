from django.db import models

from core.models import AbsProfile

class FarmerProfile(AbsProfile):

    @property
    def stringify_profile_type(self):
        return "фермера"

    # service_zone = models.CharField(verbose_name="Населенный пункт (Зона обслуживания)", max_length=1000)
    # name = models.CharField(verbose_name="Имя", max_length=200)
    # phone = models.CharField(verbose_name="Телефон", max_length=15, blank=True)

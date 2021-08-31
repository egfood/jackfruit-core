from django.db import models

from core.models import AbsProfile


class BuyerProfile(AbsProfile):
    stringify_profile_type = "покупателя"
    region = models.CharField(verbose_name='Регион', max_length=255, blank=True)

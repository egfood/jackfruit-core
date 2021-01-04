from django.db import models


class FoodAbstract(models.Model):
    class Meta:
        abstract = True

    date_creation = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Изменен", auto_now=True)
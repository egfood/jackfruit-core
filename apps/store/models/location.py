from django.db import models

from core.models import FoodAbstract


class LocationAbstract(FoodAbstract):
    class Meta:
        abstract = True

    CITY_TYPE_CHOICES = (
        ('city', 'город'),
        ('settlement', 'поселок'),
        ('village', 'деревня'),
    )

    CITY_DISTINCT_CHOICES = (
        ('angarskaya', 'Ангарская'),
        ('zelonyy_lug', 'Зелёный Луг'),
    )

    STREET_TYPE_CHOICES = (
        ('street', 'улица'),
        ('proezd', 'проезд'),
        ('avenue', 'проспект'),
        ('square', 'площадь'),
        ('side_street', 'переулок'),
        ('other', 'другое'),
    )

    city_type = models.CharField('Тип населенного пункта', max_length=100, choices=CITY_TYPE_CHOICES,
                                 default=CITY_TYPE_CHOICES[0][0])
    city_value = models.CharField('Населенный пункт', max_length=200, default='Минск')
    city_district = models.CharField('Микрорайон', max_length=200, choices=CITY_DISTINCT_CHOICES, blank=True,
                                     default='')

    street_type = models.CharField("Тип участка города", max_length=40, choices=STREET_TYPE_CHOICES,
                                   default=STREET_TYPE_CHOICES[0][0])
    street_value = models.CharField("Название улицы/площади/проезда", max_length=300)

    building = models.CharField('Дом/Строение (с корпусом)', max_length=15)

    sort_key = models.PositiveIntegerField('Сортировка', default=0)

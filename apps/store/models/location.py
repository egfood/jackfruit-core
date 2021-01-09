from django.conf import settings
from django.db import models

from core.models import FoodAbstract


class Location(FoodAbstract):
    SHORT_NAME_CHOICES = settings.OFFICES_SHORT_NAME_CHOICES

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

    LOCATION_TYPE_CHOICES = (
        ('private', 'частный'),
        ('office', 'офис'),
    )

    location_type = models.CharField('Тип адреса', max_length=10, choices=LOCATION_TYPE_CHOICES,
                                     default=LOCATION_TYPE_CHOICES[0][0])

    name = models.CharField('Имя', max_length=200)
    phone = models.CharField("Телефон", max_length=15)

    office_name = models.TextField('Короткое название офиса', max_length=settings.OFFICES_SHORT_NAME_LENGTH,
                                   default='', blank=True)

    city_type = models.CharField('Тип населенного пункта', max_length=100, choices=CITY_TYPE_CHOICES,
                                 default=CITY_TYPE_CHOICES[0][0])
    city_value = models.CharField('Населенный пункт', max_length=200, default='Минск')
    city_district = models.CharField('Микрорайон', max_length=200, choices=CITY_DISTINCT_CHOICES, blank=True,
                                     default='')

    street_type = models.CharField("Тип участка города", max_length=40, choices=STREET_TYPE_CHOICES,
                                   default=STREET_TYPE_CHOICES[0][0])
    street_value = models.CharField("Название улицы/площади/проезда", max_length=300)

    building = models.CharField('Дом/Строение (с корпусом)', max_length=15)
    porch = models.CharField('Подъезд', max_length=15, blank=True, default='')
    floor = models.CharField('Этаж', max_length=5, blank=True, default='')
    room = models.CharField('Помещение/квартира', max_length=10, blank=True, default='')

    sort_key = models.PositiveIntegerField('Сортировка', default=0)

    def is_private(self):
        return self.location_type == self.LOCATION_TYPE_CHOICES[0][0]

    def is_office(self):
        return self.location_type == self.LOCATION_TYPE_CHOICES[1][0]

    def __str__(self):
        if self.location_type == 'office':
            result = f'Офис {self.office_name}#{self.id}'
        elif self.location_type == 'private':
            result = f'{self.get_street_type_display()} {self.street_value}'
            if self.building:
                result += f' {self.building}'
            if self.porch:
                result += f' п.{self.porch}'
            if self.floor:
                result += f' эт.{self.floor}'
            if self.room:
                result += f' кв.{self.room}'
            if self.city_district:
                result += f'[{self.city_district}]'
        else:
            result = f'Неопределенный адрес #{self.id}'
        return result

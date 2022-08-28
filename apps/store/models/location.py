from functools import cached_property

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from core.models import FoodAbstract, GreenUser
from core.status_engine import StatusEnum


class LocationStatus(StatusEnum):
    private = 'частный'
    office = 'офис'


class Location(FoodAbstract):
    SHORT_NAME_CHOICES = settings.OFFICES_SHORT_NAME_CHOICES

    LOCATION_TYPE_CHOICES = LocationStatus

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

    location_type = models.CharField('Тип адреса', max_length=10, choices=LocationStatus.get_as_list(),
                                     default=LocationStatus.private.name)

    name = models.CharField('Имя', max_length=200, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, null=True, blank=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", default=None, blank=True,
                             on_delete=models.SET_NULL, null=True)

    def is_private(self):
        return self.location_type == self.LOCATION_TYPE_CHOICES.private.name

    def is_office(self):
        return self.location_type == self.LOCATION_TYPE_CHOICES.office.name

    def __str__(self):
        if self.is_office():
            result = f'Офис {self.office_name}' if self.office_name else f'Офис #{self.id}'
        elif self.is_private():
            result = f'{self.get_street_type_display()} {self.street_value}'
            if self.building:
                result += f' - {self.building}'
            if self.porch:
                result += f' п.{self.porch}'
            if self.floor:
                result += f' эт.{self.floor}'
            if self.room:
                result += f' {"кв." if self.is_private() else "оф."} {self.room}'
            if self.city_district:
                result += f'[{self.city_district}]'
        else:
            result = f'Неопределенный адрес #{self.id}'
        return result

    @cached_property
    def short_address(self):
        return self.__str__()

    @cached_property
    def full_address(self):
        result = f'[{self.get_location_type_display()}] т. {self.phone} '
        if self.is_office():
            result += f'{self.office_name} [{self.city_district}]'
        elif self.is_private():
            result += f'{self.get_street_type_display()} {self.street_value}'
            if self.building:
                result += f' - {self.building}'
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

    @classmethod
    def get_user_locations(cls, user: GreenUser) -> QuerySet:
        return cls.objects.filter(user=user)

    @cached_property
    def short_name(self):
        if self.is_office():
            return f"Офис #{self.id} {self.office_name}"
        elif self.is_private():
            return f"Частный #{self.id} пользователя {self.user}"
        else:
            return f'Неопределенный адрес #{self.id}'

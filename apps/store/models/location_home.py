from django.db import models

from .location import LocationAbstract


class HomeLocation(LocationAbstract):
    porch = models.CharField('Подъезд', max_length=15, blank=True, default='')
    floor = models.CharField('Этаж', max_length=5, blank=True, default='')
    room = models.CharField('Помещение/квартира', max_length=10, blank=True, default='')

    def __str__(self):
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
        return result

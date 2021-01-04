from django.db import models

from .location import LocationAbstract


class HomeLocation(LocationAbstract):
    porch = models.CharField('Подъезд', max_length=15, blank=True, default='')
    floor = models.CharField('Этаж', max_length=5, blank=True, default='')
    room = models.CharField('Помещение/квартира', max_length=10, blank=True, default='')

from django.conf import settings
from django.db import models

from core.models.base import FoodAbstract
from .delivery import FoodDelivery
from .location_home import HomeLocation
from .location_office import OfficeLocation
from .product import FoodProduct


class FoodOrderAbstract(FoodAbstract):
    class Meta:
        abstract = True
        indexes = (
            models.Index(fields=['delivery', 'user']),
        )

    ORDER_STATE_CHOICES = (
        ('awaiting_processing', 'Ожидает обработки'),
        ('prepared', 'Заказ сформирован'),
        ('delivered', 'Заказ доставлен'),
        ('cancelled', 'Заказ отменен'),
    )

    delivery = models.ForeignKey(FoodDelivery, verbose_name='Доставка', related_name='%(class)s_order',
                                 on_delete=models.CASCADE)
    state = models.CharField(verbose_name='Статус заказа', max_length=85, choices=ORDER_STATE_CHOICES,
                             default=ORDER_STATE_CHOICES[0][0])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                             related_name='%(app_label)s_%(class)s_order', on_delete=models.CASCADE)


class FoodOfficeOrder(FoodOrderAbstract):
    office = models.ForeignKey(OfficeLocation, verbose_name='Офис', related_name='office_order',
                               on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[в офис]'


class FoodHomeOrder(FoodOrderAbstract):
    home = models.ForeignKey(HomeLocation, verbose_name='Домашний адрес', related_name='office_order',
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[домой]'


class FoodOrderItem(FoodAbstract):
    class Meta:
        abstract = True

    product = models.ForeignKey(FoodProduct, verbose_name='Продукт', related_name='%(class)s_order_item',
                                on_delete=models.CASCADE)
    value = models.PositiveIntegerField(verbose_name='Масса продукта (от покупателя) (гр.)', blank=True, null=True)
    actual_value = models.PositiveIntegerField(verbose_name='Фактическая масса продукта (гр.)', blank=True, null=True)

    @classmethod
    def get_user_order_items(cls, request, delivery):
        order_model = cls.get_order_fk()
        order = order_model.objects.filter(delivery=delivery, user=request.user).first()
        if order is not None:
            query_set = FoodOrderItem.objects.filter(order=order)
            return query_set

    @classmethod
    def get_order_fk(cls):
        has_office_fk = hasattr(cls, 'office_order')
        has_home_fk = hasattr(cls, 'home_order')
        is_one_link_to_order_only = all([has_office_fk or has_home_fk, not has_office_fk and not has_home_fk])
        assert is_one_link_to_order_only

        if has_office_fk:
            return getattr(cls, 'office_order')
        if has_home_fk:
            return getattr(cls, 'home_order')

    def get_item_total(self):
        value = self.value if self.actual_value is None else self.actual_value
        return round(value * self.product.price / int(self.product.weight_per_price), 2)


class FoodOfficeOrderItem(FoodOrderItem):
    class Meta:
        constraints = (
            models.UniqueConstraint(fields=['office_order', 'product'], name='each_office_order_item'),
        )

    office_order = models.ForeignKey(FoodOfficeOrder, verbose_name='Заказ в офис', related_name='office_order_item',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return f'Позиция {self.value} гр. {self.product}[{self.office_order}]'


class FoodHomeOrderItem(FoodOrderItem):
    class Meta:
        constraints = (
            models.UniqueConstraint(fields=['home_order', 'product'], name='each_home_order_item'),
        )

    home_order = models.ForeignKey(FoodHomeOrder, verbose_name='Заказ домой', related_name='home_order_item',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f'Позиция {self.value} гр. {self.product}[{self.home_order}]'

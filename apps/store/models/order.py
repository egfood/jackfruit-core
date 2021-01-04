from django.conf import settings
from django.db import models

from core.models.base import FoodAbstract
from .delivery import FoodDelivery
from .location_home import HomeLocation
from .location_office import OfficeLocation
from .product import FoodProduct


class FoodOrderAbstract(FoodAbstract):
    _order_total = None
    _order_item_related_name = None

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

    @property
    def total(self):
        if self._order_total is None:
            order_items_realted_manager = getattr(self, self._order_item_related_name)
            all_order_items = order_items_realted_manager.all()
            self._order_total = sum([order_item.item_total for order_item in all_order_items])
        return self._order_total


class FoodOfficeOrder(FoodOrderAbstract):
    _order_item_related_name = 'office_order_item'

    office = models.ForeignKey(OfficeLocation, verbose_name='Офис', related_name='office_order',
                               on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[в офис]'

    @property
    def total(self):
        return super().total + settings.SHIPPING_COST


class FoodHomeOrder(FoodOrderAbstract):
    _order_item_related_name = 'home_order_item'

    home = models.ForeignKey(HomeLocation, verbose_name='Домашний адрес', related_name='office_order',
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[домой]'


class FoodOrderItem(FoodAbstract):
    _item_total = None

    class Meta:
        abstract = True

    product = models.ForeignKey(FoodProduct, verbose_name='Продукт', related_name='%(class)s_order_item',
                                on_delete=models.CASCADE)
    value = models.PositiveIntegerField(verbose_name='Масса (от покупателя) (г.)', blank=True, null=True)
    actual_value = models.PositiveIntegerField(verbose_name='Фактическая масса (г.)', blank=True, null=True)

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

    @property
    def item_total(self):
        if self._item_total is None:
            value = self.value if self.actual_value is None else self.actual_value
            self._item_total = round(value * self.product.price / int(self.product.weight_per_price), 2)
        return self._item_total


class FoodOfficeOrderItem(FoodOrderItem):
    _delivery_short_name = None

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=['office_order', 'product'], name='each_office_order_item'),
        )

    office_order = models.ForeignKey(FoodOfficeOrder, verbose_name='Заказ в офис', related_name='office_order_item',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return f'Позиция {self.value} г. {self.product}[{self.office_order}]'

    @property
    def delivery_short_name(self):
        if self._delivery_short_name is None:
            self._delivery_short_name = f"Дост. {self.office_order.delivery.short_name} (в офис)"
        return self._delivery_short_name


class FoodHomeOrderItem(FoodOrderItem):
    _delivery_short_name = None

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=['home_order', 'product'], name='each_home_order_item'),
        )

    home_order = models.ForeignKey(FoodHomeOrder, verbose_name='Заказ домой', related_name='home_order_item',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f'Позиция {self.value} г. {self.product}[{self.home_order}]'

    @property
    def delivery_short_name(self):
        if self._delivery_short_name is None:
            self._delivery_short_name = f"Дост. {self.home_order.delivery.short_name} (домой)"
        return self._delivery_short_name

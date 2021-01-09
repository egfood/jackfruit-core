from django.conf import settings
from django.db import models

from core.models.base import FoodAbstract
from .delivery import FoodDelivery
from .product import FoodProduct


class FoodOrderAbstract(FoodAbstract):
    _order_cost = None
    _order_item_related_name = None
    _order_weight = None
    _text_order_weight = None
    _text_delivery = None
    _text_user = None
    _order_items_related = None

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
    def total_cost(self):
        if self._order_cost is None:
            self._order_cost = sum([order_item.item_total for order_item in self.order_items_related])
        return self._order_cost

    @property
    def total_weight(self):
        if self._order_weight is None:
            self._order_weight = sum([order_item.weight for order_item in self.order_items_related])
        return self._order_weight

    @property
    def text_total_weight(self):
        if self._text_order_weight is None:
            total_weight = sum([order_item.weight for order_item in self.order_items_related])
            self._text_order_weight = f"{total_weight} {settings.WEIGHT_UNIT_ABBREVIATION}"
        return self._text_order_weight

    @property
    def text_delivery(self):
        if self._text_delivery is None:
            self._text_delivery = self.delivery.short_name
        return self._text_delivery

    @property
    def text_user(self):
        if self._text_user is None:
            user = self.user
            self._text_user = f"{user.first_name}({user.email})"
        return self._text_user

    # TODO: will be implemented after add phone to Green User model
    @property
    def text_phone(self):
        return

    @property
    def order_items_related(self):
        if self._order_items_related is None:
            order_items_realted_manager = getattr(self, self._order_item_related_name)
            self._order_items_related = order_items_realted_manager.all()
        return self._order_items_related


class FoodOfficeOrder(FoodOrderAbstract):
    _order_item_related_name = 'office_order_item'

    office = models.ForeignKey(OfficeLocation, verbose_name='Офис', related_name='office_order',
                               on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[в офис]'


class FoodHomeOrder(FoodOrderAbstract):
    _order_item_related_name = 'home_order_item'

    home = models.ForeignKey(HomeLocation, verbose_name='Домашний адрес', related_name='office_order',
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery} для {self.user}[домой]'

    @property
    def total_cost(self):
        return super().total_cost + settings.SHIPPING_COST


class FoodOrderItem(FoodAbstract):
    _item_total = None
    _weight = None
    _text_weight = None

    class Meta:
        abstract = True

    product = models.ForeignKey(FoodProduct, verbose_name='Продукт', related_name='%(class)s_order_item',
                                on_delete=models.CASCADE)
    value = models.PositiveIntegerField(verbose_name=f'Масса (от покупателя) ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                        blank=True, null=True)
    actual_value = models.PositiveIntegerField(verbose_name=f'Фактическая масса ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                               blank=True, null=True)

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
            self._item_total = round(self.weight * self.product.price / int(self.product.weight_per_price), 2)
        return self._item_total

    @property
    def weight(self):
        if self._weight is None:
            self._weight = self.value if self.actual_value is None else self.actual_value
        return self._weight

    @property
    def text_weight(self):
        if self._text_weight is None:
            self._text_weight = f"{self.weight} {settings.WEIGHT_UNIT_ABBREVIATION}"
        return self._text_weight

    @property
    def text_safety_weight(self):
        base = self.text_weight
        if self.actual_value:
            base += "[ФАКТ.]"
        return base


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

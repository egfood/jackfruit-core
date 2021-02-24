import csv
import logging
from abc import ABC
from collections import defaultdict
from itertools import groupby
from operator import attrgetter
from typing import Iterable

from django.conf import settings
from django.db.models import QuerySet

from .core import BasicCSVAssembler
# from ..models import FoodOfficeOrder, FoodHomeOrder, FoodOfficeOrderItem, FoodHomeOrderItem

log = logging.getLogger(__name__)


# class OrdersCSVAssembler(BasicCSVAssembler):
#     unique_filename_part = 'orders'

#     def build_csv_file(self):
#         home_orders, office_orders = self.get_csv_data(self.selected_instance)
#         order_extractor = FieldsExtractor(settings.CSV_EXPORT_COLUMN_NAMES["ORDERS_IN_DELIVERY"])
#         order_position_extractor = FieldsExtractor(settings.CSV_EXPORT_COLUMN_NAMES["ORDER_POSITION_IN_DELIVERY"])
#         writer = csv.writer(self.responder.csv_file_response, dialect="excel")
#         mixed_orders = home_orders | office_orders
#         for order, order_items in mixed_orders.items():
#             order_headers = order_extractor.headers(order)
#             writer.writerow(order_headers)
#             writer.writerow(order_extractor.get_field_values(order))
#             if isinstance(order_items, Iterable):
#                 writer.writerow(self.add_shift(order_position_extractor.headers(order_items[0])))
#                 for position in order_items:
#                     writer.writerow(self.add_shift(order_position_extractor.get_field_values(position)))
#                 writer.writerow(["---" for _ in range(len(order_headers))])
#             else:
#                 log.error(f'Order #{order.id} have no OrderItems.')
#
#
#     @staticmethod
#     def add_shift(_list, shift_str="-"):
#         _list.insert(0, shift_str)
#         return _list
#
#     def get_csv_data(self, delivery):
#         home_orders = FoodHomeOrder.objects.filter(delivery=delivery)
#         office_orders = FoodOfficeOrder.objects.filter(delivery=delivery)
#         return self._combine_items_by_orders("home_order", home_orders, FoodHomeOrderItem), \
#                self._combine_items_by_orders("office_order", office_orders, FoodOfficeOrderItem)
#
#     def _combine_items_by_orders(self, combine_key: str, orders: QuerySet, source_model) -> defaultdict:
#         filter_kwargs = {f"{combine_key}__in": orders}
#         items_by_orders = groupby(source_model.objects.filter(**filter_kwargs).order_by(combine_key),
#                                   key=attrgetter(combine_key))
#         combined_result = defaultdict(list)
#         for order, items in items_by_orders:
#             combined_result[order] = list(items)
#         return combined_result
#
#
# class FieldsExtractor(ABC):
#
#     def __init__(self, fields_setting):
#         self.fields_setting = fields_setting
#
#     def headers(self, instance_example):
#         return [header for attr, header in self.fields_setting.items() if hasattr(instance_example, attr)]
#
#     def get_field_values(self, instance):
#         return [getattr(instance, field_name) for field_name in self.fields_setting.keys() if
#                 hasattr(instance, field_name)]

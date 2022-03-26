import csv

from django.conf import settings

from .core import BasicCSVAssembler
from ..models import FoodOrder, FoodOrderItem, FarmerProduct


class ProductsCSVAssembler(BasicCSVAssembler):
    unique_filename_part = 'products'

    def build_csv_file(self):
        column_names, csv_rows = self.get_csv_data(self.selected_instance)
        writer = csv.DictWriter(self.responder.csv_file_response, fieldnames=column_names.keys(), dialect="excel")
        writer.writerow(column_names)
        writer.writerows(csv_rows)

    def get_csv_data(self, delivery):
        settings_field_names = settings.CSV_EXPORT_COLUMN_NAMES["PRODUCTS_IN_DELIVERY"]
        field_names_keys = settings_field_names.keys()

        search_orders = FoodOrder.objects.filter(delivery=delivery)
        search_order_items = FoodOrderItem.objects.filter(order__in=search_orders.values_list('pk', flat=True))
        pk_of_products = set(search_order_items.values_list('product_id', flat=True))
        products_in_delivery = FarmerProduct.objects.filter(pk__in=pk_of_products)

        csv_rows = []
        for p in products_in_delivery:
            current_row = {}
            for product_field in p._meta.fields:
                if product_field.name in field_names_keys:
                    current_row[product_field.name] = getattr(p, product_field.name)

            order_items_by_product = search_order_items.filter(product=p)
            if 'price_by_weight' in field_names_keys:
                current_row['price_by_weight'] = f'{p.price} BYN за {p.unit}'
            if 'total_weight' in field_names_keys:
                weights = [item.weight for item in
                           list(order_items_by_product)]
                current_row['total_weight'] = f'{sum(weights)} {p.unit}.'
            if 'total_price' in field_names_keys:
                prices = [item.item_total for item in
                          list(order_items_by_product)]
                current_row['total_price'] = f'{sum(prices)} BYN'
            if 'orders_count' in field_names_keys:
                current_row['orders_count'] = len(order_items_by_product)
            csv_rows.append(current_row)

        return settings_field_names, csv_rows

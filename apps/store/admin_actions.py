import csv

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from .models import FoodProduct, FoodOfficeOrder, FoodHomeOrder, FoodOfficeOrderItem, FoodHomeOrderItem


class ExportProductsToCSVMixin:
    _response = None

    def export_products_to_csv(self, request, queryset):
        if len(queryset) == 1:
            delivery = queryset[0]
            self._response = self.get_response_as_csv_file(delivery)
            self.build_csv(delivery)
            return self._response
        else:
            messages.error(request, 'Выгрузка продуктов доставки возможна только для одной выбранной доставки.')

    export_products_to_csv.short_description = "CSV экспорт продуктов в доставке"

    def get_response_as_csv_file(self, delivery):
        response = HttpResponse(content_type="text/csv")
        now = timezone.now()
        filename = f"delivery_{delivery.pk}_products_{now:%d-%m-%Y-%Hh-%Mm-%Ss}"
        response["Content-Disposition"] = f"attachment; filename={filename}.csv"
        return response

    def build_csv(self, delivery):
        column_names, csv_rows = self.get_csv_data(delivery)
        writer = csv.DictWriter(self._response, fieldnames=column_names.keys(), dialect="excel")
        writer.writerow(column_names)
        writer.writerows(csv_rows)

    def get_csv_data(self, delivery):
        settings_field_names = settings.MODEL_FIELD_NAMES_FOR_CSV_EXPORT_PRODUCTS_IN_DELIVERY.keys()

        office_orders = FoodOfficeOrder.objects.filter(delivery=delivery)
        home_orders = FoodHomeOrder.objects.filter(delivery=delivery)
        office_order_items = FoodOfficeOrderItem.objects.filter(office_order__in=office_orders.values_list('pk',
                                                                                                           flat=True))
        home_order_items = FoodHomeOrderItem.objects.filter(home_order__in=home_orders.values_list('pk', flat=True))

        pk_of_products = set(office_order_items.values_list('product_id', flat=True))
        pk_of_products.update(home_order_items.values_list('product_id', flat=True))
        products_in_delivery = FoodProduct.objects.filter(pk__in=pk_of_products)

        csv_rows = []
        for p in products_in_delivery:
            current_row = {}
            for product_field in p._meta.fields:
                if product_field.name in settings_field_names:
                    current_row[product_field.name] = getattr(p, product_field.name)

            office_order_items_by_product = office_order_items.filter(product=p)
            home_order_items_by_product = home_order_items.filter(product=p)
            if 'price_by_weight' in settings_field_names:
                current_row['price_by_weight'] = f'{p.price} BYN за {p.get_weight_per_price_display()}'
            if 'total_weight' in settings_field_names:
                weights = [item.weight for item in
                           list(office_order_items_by_product) + list(home_order_items_by_product)]
                current_row['total_weight'] = f'{sum(weights)} г.'
            if 'total_price' in settings_field_names:
                prices = [item.item_total for item in
                          list(office_order_items_by_product) + list(home_order_items_by_product)]
                current_row['total_price'] = f'{sum(prices)} BYN'
            if 'orders_count' in settings_field_names:
                current_row['orders_count'] = len(office_order_items_by_product) + len(home_order_items_by_product)

            csv_rows.append(current_row)

        return settings.MODEL_FIELD_NAMES_FOR_CSV_EXPORT_PRODUCTS_IN_DELIVERY, csv_rows

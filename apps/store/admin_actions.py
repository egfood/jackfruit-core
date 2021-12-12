import functools

from django.contrib import messages
from django.http import HttpResponseRedirect

from .csv_export.order_and_items import OrdersCSVAssembler
from .csv_export.products import ProductsCSVAssembler


def selected_instance_single_check(error_message):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            _, request, queryset = args
            if len(queryset) > 1:
                messages.error(request, error_message)
                return HttpResponseRedirect(request.path_info)
            return method(*args, **kwargs)

        return wrapper

    return decorator


class ExportCSVMixin:

    @selected_instance_single_check("Выгрузка продуктов доставки возможна только для одной выбранной доставки.")
    def export_products_to_csv(self, request, queryset):
        csv_assembler = ProductsCSVAssembler(queryset[0])
        csv_assembler.build_csv_file()
        return csv_assembler.responder.csv_file_response

    export_products_to_csv.short_description = "CSV экспорт продуктов в доставке"

    @selected_instance_single_check("Выгрузка продуктов доставки возможна только для одной выбранной доставки.")
    def export_detail_orders_to_csv(self, request, queryset):
        csv_assembler = OrdersCSVAssembler(queryset[0])
        csv_assembler.build_csv_file()
        return csv_assembler.responder.csv_file_response

    export_detail_orders_to_csv.short_description = "Детализированный экспорт заказов в CSV"

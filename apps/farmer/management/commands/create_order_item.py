import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.store.models import order_item, order
from apps.farmer.models.product import FarmerProduct


class Command(BaseCommand):
    help = u'Create a ORDER ITEM'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help=u'Number of created Order items')
        parser.add_argument('--call',
                            action='store_true',
                            default=False,
                            help='Used when sending a command through call_command(launch creation_tree)')

    def handle(self, *args, **options):
        total = options['total']
        if FarmerProduct.objects.all().exists() or order.FoodOrder.objects.all().exists():
            call_command('create_food_order', f'--total=1')
            call_command('create_farmer_product', f'--total=1')
        selected_farmer_product = FarmerProduct.objects.order_by('-date_creation')[0]
        selected_food_order = order.FoodOrder.objects.order_by('-date_creation')[0]
        for i in range(total):
            try:
                order_item_instance = order_item.FoodOrderItem.objects.create(product=selected_farmer_product,
                                                                              value=random.randint(1, 1000000),
                                                                              actual_value=random.randint(1, 100000),
                                                                              order=selected_food_order)
                self.stdout.write(self.style.SUCCESS(f'Order item for delivery '
                                                     f'{order_item_instance.order.delivery} created'))
            except IntegrityError:
                self.stdout.write(self.style.SUCCESS(f'Order item for delivery no created'))

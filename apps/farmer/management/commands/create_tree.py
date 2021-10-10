from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create all models instances'

    def handle(self, *args, **options):
        call = True
        options_list = [
            ('create_farmer_profile', '--total=1'),
            ('create_product_category', '--total=1'),
            ('create_root_product', '--total=1'),
            ('create_farmer_product', '--call', '--total=1'),
            ('create_food_order', '--total=1'),
            ('create_order_item', '--call', '--total=1'),
            ('create_feedback', '--call', '--total=1')
        ]
        for i in options_list:
            call_command(*i)


from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.farmer.models import product, profile
from apps.store.models.product import RootProduct

import random


class Command(BaseCommand):
    help = 'Create a FARMER PRODUCT'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Farmer product')

        parser.add_argument('--call',
                            action='store_true',
                            default=False,
                            help='Used when sending a command through call_command(launch creation_tree)')

    def handle(self, *args, **options):
        total = options['total']
        if profile.FarmerProfile.objects.all().exists() or RootProduct.objects.all().exists():
            call_command('create_farmer_profile', '--total=1')
            call_command('create_root_product', '--total=1')
        if options['call']:
            selected_farmer_profile = profile.FarmerProfile.objects.order_by('-date_creation')[0]
            selected_root_product = RootProduct.objects.order_by('-date_creation')[0]

        else:
            selected_farmer_profile = random.choice(profile.FarmerProfile.objects.all())
            selected_root_product = random.choice(RootProduct.objects.all())
        for i in range(total):
            unit_random = random.randint(0, 3)
            size_random = random.randint(0, 2)
            price_random = round(random.uniform(0.01, 100), 2)
            value_random = round(random.uniform(0.01, 1000), 2)
            try:
                farmer_product_instance = product.FarmerProduct.objects.create(
                    farmer=selected_farmer_profile,
                    product=selected_root_product, value=value_random,
                    unit=product.FarmerProduct.UNIT_PRODUCT[unit_random][0],
                    size=product.FarmerProduct.SIZE_CHOICES[size_random][0],
                    price=price_random
                )
                self.stdout.write(self.style.SUCCESS(f'farmer product for root product '
                                                     f'{farmer_product_instance.product.name} created'))
            except IntegrityError:
                self.stdout.write(self.style.SUCCESS(f'farmer product for root product not created'))

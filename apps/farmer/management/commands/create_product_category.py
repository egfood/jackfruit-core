import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.store.models.product_category import ProductCategory


class Command(BaseCommand):
    help = 'Create a PRODUCT CATEGORY'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Product Category')

    def handle(self, *args, **options):
        total = options['total']
        name_lst = ['Овощи', 'Ягоды', "Фрукты", "Корнеплоды", "Семена", "Зелень"]
        try:
            for i in range(total):
                name = random.choice(name_lst)
                product_category = ProductCategory.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f'Product Category {product_category.name} created'))
        except IntegrityError:
            self.stdout.write(self.style.SUCCESS(f'Product Category not created'))

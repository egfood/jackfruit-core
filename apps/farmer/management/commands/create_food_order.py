from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.store.models import order, delivery, location
from apps.buyer.models import profile

import random


class Command(BaseCommand):
    help = 'Create a FOOD ORDER'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Food orders')

    def handle(self, *args, **options):
        total = options['total']
        call_command('create_delivery', f'--total={total}')
        call_command('create_buyer_profile', f'--total={total}')
        call_command('create_location', f'--total={total}')
        _selected_delivery = delivery.FoodDelivery.objects.order_by('-date_creation')[:total]
        _selected_buyer = profile.BuyerProfile.objects.order_by('-date_creation')[:total]
        _selected_location = location.Location.objects.order_by('-date_creation')[:total]
        for i in range(total):
            selected_delivery = _selected_delivery[i]
            selected_buyer = _selected_buyer[i]
            selected_location = _selected_location[i]
            try:
                food_order_instance = order.FoodOrder.objects.create(
                    delivery=selected_delivery,
                    state=random.choice(order.FoodOrder.ORDER_STATE.get_as_list())[0],
                    buyer=selected_buyer,
                    location=selected_location)
                self.stdout.write(self.style.SUCCESS(f'FoodOrder created for buyer {selected_buyer.name} '
                                                     f'delivery {selected_delivery.date}'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f'FoodOrder not created'))

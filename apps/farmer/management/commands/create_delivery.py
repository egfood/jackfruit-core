import datetime
import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.store.models import delivery


class Command(BaseCommand):
    help = 'Create a DELIVERY'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created deliveries')

    def handle(self, *args, **options):
        total = options['total']
        delivery_date = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=9999)
        try:
            for i in range(total):
                created_delivery = delivery.FoodDelivery.objects.create(
                    date=delivery_date,
                    state=random.choice(delivery.FoodDelivery.DELIVERY_STATE_CHOICES[0])
                )
                self.stdout.write(self.style.SUCCESS(f" Delivery with status {created_delivery.state}"
                                                     f" created {created_delivery.date}"))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f"Delivery not created"))

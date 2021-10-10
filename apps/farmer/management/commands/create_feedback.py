from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.farmer.models import feedback
from apps.store.models.order_item import FoodOrderItem

import random
import datetime


class Command(BaseCommand):
    help = 'Create a FEEDBACK'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Feedback')
        parser.add_argument('--call',
                            action='store_true',
                            default=False,
                            help='Используется при отправке команды через call_command(запуск создания мз create_tree)')

    def handle(self, *args, **options):
        total = options['total']
        if options['call']:
            selected_order_item = FoodOrderItem.objects.order_by('-date_creation')[:1]
        else:
            call_command('create_order_item', f'--total={total}')
            selected_order_item = FoodOrderItem.objects.order_by('-date_creation')[:total]
        for i in selected_order_item:
            try:
                feedback_instance = feedback.FarmerFeedback.objects.create(
                    rating=random.randint(1, 5),
                    feedback=f"Какой-то отзыв,"
                             f" создан {datetime.datetime.today().strftime('%Y-%m-%d-%H.%M.%S')}",
                    order_item=i)
                self.stdout.write(self.style.SUCCESS(f"Feedback {i} created"))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f"Feedback not created"))

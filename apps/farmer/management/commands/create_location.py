import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from .generators import email_gen
from apps.store.models import location
from core.models import user


class Command(BaseCommand):
    help = 'Create LOCATION'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created locations')

    def handle(self, *args, **options):
        total = options['total']
        user_password = '11111QqQ'
        if user.GreenUser.objects.all().count() == 0:
            try:
                created_user = user.GreenUser.objects.create_user(email=email_gen(),
                                                                  password=user_password,
                                                                  is_active=True)
            except IntegrityError:
                self.stdout.write(self.style.ERROR('GreenUser not created'))
        selected_user = random.choice(user.GreenUser.objects.all())
        try:
            for i in range(total):
                location.Location.objects.create(
                    location_type=random.choice(location.Location.LOCATION_TYPE_CHOICES.get_as_list())[0],
                    name='user',
                    phone=''.join(['25' or '29' or '33' or '44',
                                   str(random.randint(1111111, 9999999))]),
                    city_type=random.choice(location.Location.CITY_TYPE_CHOICES)[0],
                    city_value='Minsk',
                    city_district=random.choice(location.Location.CITY_DISTINCT_CHOICES)[0],
                    street_type=random.choice(location.Location.STREET_TYPE_CHOICES)[0],
                    street_value='',
                    building='1',
                    user=selected_user
                )
                self.stdout.write(self.style.SUCCESS(f'Location for user {selected_user} created'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR('Location not created'))

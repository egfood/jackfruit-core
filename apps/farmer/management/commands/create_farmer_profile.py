import random
import string

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.farmer.models.profile import FarmerProfile
from core.models import user
from .create_buyer_profile import name_gen


def email_gen():
    random_user_email = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
    return f'{random_user_email}@mailforspam.com'


class Command(BaseCommand):
    help = 'Create a FARMER PROFILE'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Farmer profiles')
        # parser.add_argument('-p', '--prefix',
        #                     type=str,
        #                     default='Farmer',
        #                     nargs='?',
        #                     help='Prefix for the created user')

    def handle(self, *args, **options):
        total = options['total']
        # prefix = options['prefix']
        user_password = '11111QqQ'
        try:
            for i in range(total):
                create_green_user = user.GreenUser.objects.create_user(email=email_gen(),
                                                                       password=user_password,
                                                                       is_active=True)
                farmer_profile = FarmerProfile.objects.create(service_zone='Minsk',
                                                              legal_name='Company Name',
                                                              user=create_green_user,
                                                              photo=None,
                                                              phone=''.join(['25' or '29' or '33' or '44',
                                                                             str(random.randint(1111111, 9999999))]),
                                                              region='Minsk',
                                                              name=name_gen())
                self.stdout.write(self.style.SUCCESS(f'Account {farmer_profile.name} was successfully created, '
                                                     f' email - {create_green_user.email}, '
                                                     f'password - {user_password}'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'Farmer profile not created'))

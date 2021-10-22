import random
import string

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from apps.buyer.models import profile
from core.models import user
from russian_names import RussianNames


def name_gen():
    random_user_name = RussianNames(count=1, patronymic=False, surname=False).get_person()
    return random_user_name


def email_gen():
    random_user_email = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
    return f'{random_user_email}@mailforspam.com'


class Command(BaseCommand):
    help = 'Create a BUYER PROFILE'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            type=int,
                            default=1,
                            help='Number of created Buyer profile')
        # parser.add_argument('-p', '--prefix',
        #                     type=str,
        #                     default='Buyer',
        #                     nargs='?',
        #                     help='Prefix for the created user')

    def handle(self, *args, **options):
        total = options['total']
        # prefix = options['prefix']
        user_password = '11111QqQ'
        try:
            for i in range(total):
                selected_green_user = user.GreenUser.objects.create_user(email=email_gen(),
                                                                         password=user_password,
                                                                         is_active=True)
                buyer_profile = profile.BuyerProfile.objects.create(
                    user=selected_green_user,
                    photo=None,
                    phone=''.join(['25' or '29' or '33' or '44',
                                   str(random.randint(1111111, 9999999))]),
                    region='Minsk',
                    name=name_gen())
                self.stdout.write(self.style.SUCCESS(f'Account {buyer_profile.name} was successfully created, '
                                                     f' email - {selected_green_user.email}, '
                                                     f'password - {user_password}'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f"Buyer profile not created"))


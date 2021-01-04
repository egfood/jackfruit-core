import timeit

from django.core.management import BaseCommand, CommandError

from core.models import DemoUserWithProfileCreator, UserCreationResult


class Command(BaseCommand):
    users_helper = DemoUserWithProfileCreator()
    OUTPUT_DECORATION_LENGTH = 32
    OUTPUT_DECORATION_SYMBOL = '-'

    help = "Creation demo users of one type ('superuser', 'buyer', 'farmer') or all types one time"

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['create', 'remove'],
            type=str,
            nargs="?",
            help="Action for users (create or remove)",
        )
        parser.add_argument(
            '--role', '-r',
            default=None,
            choices=self.users_helper.USER_ROLES,
            nargs="?",
            help="Type of created user (create or remove). Choose one of user role to create",
        )
        parser.add_argument(
            '--count', '-c',
            type=int,
            default=1,
            help='Count of created users',
        )
        parser.add_argument(
            '--index', '-i',
            type=int,
            default=1,
            help='Index for first created user each type',
        )

    def handle(self, *args, **options):
        if options['action'] is None:
            raise CommandError(self.style.ERROR('Action argument (create or remove) must be specified'))
        elif options['action'] == 'create':
            self.create_users_and_show_time(**options)
        elif options['action'] == 'remove':
            # TODO: implement remove users
            pass

    def create_users_and_show_time(self, **kwargs):
        start_time = timeit.default_timer()
        result = self.users_helper.create_demo_users(**kwargs)
        end_time = timeit.default_timer()
        elapsed_time_in_seconds = round((end_time - start_time), 2)
        self.print_result(result)
        self.stdout.write(f"Command execution completed in {elapsed_time_in_seconds}s")

    def print_result(self, results: list) -> None:
        self.stdout.write(self.style.ERROR(
            'Demo users creation'.center(self.OUTPUT_DECORATION_LENGTH, self.OUTPUT_DECORATION_SYMBOL)))
        self.stdout.write(self.style.SUCCESS(f'password = {DemoUserWithProfileCreator.USER_PASSWORD}\n'))
        for r in results:
            if r.has_errors:
                self.print_fail(r.error)
            else:
                self.print_success(r)
        self.stdout.write(self.style.ERROR(''.center(self.OUTPUT_DECORATION_LENGTH, self.OUTPUT_DECORATION_SYMBOL)))

    def print_fail(self, message: str) -> None:
        self.stdout.write(self.style.ERROR(f"User can't create. {message}"))

    def print_success(self, result: UserCreationResult) -> None:
        self.stdout.write(self.style.SUCCESS(result.created_user))

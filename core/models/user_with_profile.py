import sys
from collections import namedtuple

from django.db import transaction, IntegrityError

from .profile import UserProfile
from .user import GreenUser

UserCreationResult = namedtuple('UserCreationResult', ['has_errors', 'error', 'created_user'])


class UserWithProfileManager:
    SUPERUSER_ROLE = 'superuser'

    def create_user_with_profile(self, **user_data) -> UserCreationResult:
        """
        :param user_data: must include user data (at least email, first_name and password)
        :return: tuple where 1st item is boolean success result, 2nd - error if exist, 3nd is created user
        """

        user_role = user_data.pop('role', UserProfile.DEFAULT_USER_ROLE)
        creation_function = self.get_user_creation_function(user_role)
        user_profile_data = {}
        if user_role != self.SUPERUSER_ROLE:
            user_profile_data['user_role'] = user_role

        try:
            with transaction.atomic():
                user = creation_function(**user_data)
        except IntegrityError as error:
            return UserCreationResult(has_errors=True, error=error, created_user=None)
        else:
            user_profile_data['user'] = user
            profile = UserProfile.objects.create(**user_profile_data)
            profile.save()
            return UserCreationResult(has_errors=False, error=None, created_user=user)

    def get_user_creation_function(self, user_role: str):
        if user_role == self.SUPERUSER_ROLE:
            return GreenUser.objects.create_superuser
        else:
            return GreenUser.objects.create_user


class TerminalMessageStyle:
    END = '\033[1;37;0m'
    RED = '\033[1;31;48m'
    GREEN = '\033[1;32;48m'

    def success(self, message: str) -> str:
        return f'{self.GREEN}{message}{self.END}'

    def error(self, message: str) -> str:
        return f'{self.RED}{message}{self.END}'


class DemoUserWithProfileCreator:
    manager = UserWithProfileManager()
    USER_ROLES = [role[0] for role in UserProfile.USER_ROLE_CHOICES] + [UserWithProfileManager.SUPERUSER_ROLE]
    EMAIL_DOMAIN = "@mailforspam.com"
    USER_PASSWORD = 'qwerty12321'
    style = TerminalMessageStyle()

    def create_demo_users(self, **kwargs) -> list:
        """
        Creation users on range from 'index' to 'index'+'count' (it's index use on name/email)
        for each user 'role' if it was defined

        :param kwargs:
            'index' - first index for username and email for first created user. '1' by default
            'count' - count of created users. '1' by default
            'role' - role for created users,
                     if role is not defined then method will create 'count' users for each role.
        :return:
        """

        start_username_index = kwargs.get('index', 1)
        users_count = kwargs.get('count', 1)

        user_role = kwargs.get('role', None)
        user_creation_results = []

        if user_role is None:
            for role in self.USER_ROLES:
                batch_result = self.create_users_in_range(start_username_index, users_count, role)
                user_creation_results.extend(batch_result)
        else:
            batch_result = self.create_users_in_range(start_username_index, users_count, self.manager.SUPERUSER_ROLE)
            user_creation_results.extend(batch_result)

        return user_creation_results

    def create_users_in_range(self, start_index: int, count: int, role: str) -> list:
        usernames = [self.get_username(role, i) for i in range(start_index, start_index + count)]
        result_data = []

        for name in usernames:
            user_data = {
                'first_name': name,
                'email': self.get_email(name),
                'role': role,
                'is_active': True,
                'password': self.USER_PASSWORD,
            }
            creation_result = self.manager.create_user_with_profile(**user_data)
            result_data.append(creation_result)

        return result_data

    @staticmethod
    def get_username(user_prefix: str, user_index: int) -> str:
        return f"{user_prefix}{str(user_index).zfill(4)}"

    def get_email(self, username: str) -> str:
        return f"{username}{self.EMAIL_DOMAIN}"

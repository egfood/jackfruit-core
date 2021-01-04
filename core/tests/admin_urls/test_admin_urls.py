from django.test import TestCase
from django.urls import reverse

from core.models import GreenUser, FoodProduct, FoodDelivery, FoodOrder


class AdminUrlsTest(TestCase):
    super_user = None
    models_for_test_in_admin = (FoodProduct, FoodDelivery, FoodOrder)
    super_user_data = {
        'tg_username': 'admin',
        'location': 'K3V',
        'password': '',
    }

    def setUp(self):
        self.super_user = GreenUser.objects.create_superuser(**self.super_user_data)
        self.client.login(tg_username=self.super_user_data['tg_username'], password=self.super_user_data['password'])

    def test_super_admin_login(self):
        root_core_admin_url = reverse('admin:app_list', args=('core',))
        response = self.client.get(root_core_admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), str(self.super_user))

    def test_admin_changelist_urls(self):
        for model in self.models_for_test_in_admin:
            url = reverse(f'admin:core_{model.__name__.lower()}_changelist')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

from apps.buyer.models.profile import BuyerProfile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import GreenUser

User = get_user_model()


class BuyerPagesTests(TestCase):
    user_data = {
        "email": "test_user@mailforspam.com",
        "password": "QWERTY12321",
        "is_active": True,
    }

    def setUp(self):
        self.user = GreenUser.objects.create_user(**self.user_data)
        buyer_profile_data = {
            "user": self.user,
            "name": "Test User",
            "phone": "+375-00000000",
        }
        # Buyer profile shady use in tests below for correct working code
        profile = BuyerProfile(**buyer_profile_data)
        profile.save()
        self.client.login(password=self.user_data["password"], email=self.user_data["email"])

    def test_cart_page_uses_correct_template(self):
        resource = self.client.get(reverse('buyer:cart'))
        self.assertTemplateUsed(resource, 'buyer/pages/buyer-cart.html')

    def test_url_cart(self):
        response = self.client.get(reverse('buyer:cart'))
        self.assertEqual(response.status_code, 200)

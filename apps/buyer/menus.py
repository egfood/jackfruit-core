from django.urls import reverse
from menu import Menu, MenuItem

# myProducts.html
Menu.add_item("buyer_left_sidebar", MenuItem("Витрина",
                                             reverse("buyer:home"),
                                             weight=10,
                                             icon="fas fa-store"))
# index.html
Menu.add_item("buyer_left_sidebar", MenuItem("Корзина",
                                             reverse("buyer:cart"),
                                             weight=20,
                                             icon="fas fa-shopping-basket"))
# payments.html
Menu.add_item("buyer_left_sidebar", MenuItem("Платежи",
                                             reverse("buyer:home"),
                                             weight=30,
                                             icon="fas fa-money-bill-wave-alt"))
# rating.html
Menu.add_item("buyer_left_sidebar", MenuItem("Рейтинг фермеров",
                                             reverse("buyer:home"),
                                             weight=40,
                                             icon="fas fa-star"))

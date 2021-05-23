from django.urls import reverse
from menu import Menu, MenuItem

# index.html
Menu.add_item("farmer_left_sidebar", MenuItem("Мои продукты",
                                              reverse("farmer:foodstuffs"),
                                              weight=10,
                                              icon="fab fa-pagelines"))
# orders.html
Menu.add_item("farmer_left_sidebar", MenuItem("Заказы",
                                              reverse("farmer:foodstuffs"),
                                              weight=20,
                                              icon="fas fa-shopping-basket"))
# payments.html
Menu.add_item("farmer_left_sidebar", MenuItem("Платежи",
                                              reverse("farmer:foodstuffs"),
                                              weight=30,
                                              icon="fas fa-money-bill-wave-alt"))
# rating.html
Menu.add_item("farmer_left_sidebar", MenuItem("Мой рейтинг",
                                              reverse("farmer:foodstuffs"),
                                              weight=40,
                                              icon="fas fa-star"))

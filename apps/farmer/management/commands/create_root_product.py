import random

from django.core.management import BaseCommand, call_command
from django.db import IntegrityError

from apps.store.models.product import RootProduct, ProductCategory
from apps.store.models.trade_margin import TradeMargin


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', '--total',
                            default=1,
                            type=int,
                            help='Create a ROOT PRODUCT')

    def handle(self, *args, **options):
        total = options['total']
        name_lst = ['Томат', 'Огурец', "Лук", "Чеснок", "Свекла", "Арбуз"]
        description = ['Свежий', 'Сочный', 'Без ГМО', 'Грунтовой', 'Натуральный', 'Без нитратов', 'Домашний', 'Вкусный',
                       'Сладкий', 'Ароматный', 'Аппетитный', 'чОткий']
        if ProductCategory.objects.all().count() == 0:
            call_command('create_product_category', '--total=1')
        selected_category = random.choice(ProductCategory.objects.all())
        trade_margin_qs = TradeMargin.objects.all()
        if trade_margin_qs.exists():
            trade_margin = trade_margin_qs[0]
        else:
            trade_margin = TradeMargin.objects.create(backoffice_margin=70.0, dev_margin=30.0)
        try:
            for i in range(total):
                name = random.choice(name_lst)
                # TODO заменить None в image на рандомное изображение
                root_product_instance = RootProduct.objects.create(
                    name=name,
                    image=None,
                    is_visible=True,
                    description=', '.join([random.choice(description) for i in range(5)]),
                    category=selected_category,
                    trade_margin=trade_margin
                )
                self.stdout.write(self.style.SUCCESS(f'RootProduct {root_product_instance.name} created'))
        except IntegrityError:
            self.stdout.write(self.style.SUCCESS(f'RootProduct not created'))

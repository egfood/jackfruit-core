# Generated by Django 3.2.6 on 2021-12-08 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0017_historicalfarmerproduct'),
        ('store', '0011_alter_foodorderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorderitem',
            name='historical_product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='farmer.historicalfarmerproduct', verbose_name='Историчный фермерский продукт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foodorderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='farmer.farmerproduct', verbose_name='Фермерский продукт'),
        ),
    ]
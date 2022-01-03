# Generated by Django 3.2.6 on 2022-01-03 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerbalance',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_balance', to='store.foodorderitem', verbose_name='Заказ'),
        ),
    ]
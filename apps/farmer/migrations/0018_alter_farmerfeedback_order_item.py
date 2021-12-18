# Generated by Django 3.2.6 on 2021-12-15 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20211208_1929'),
        ('farmer', '0017_historicalfarmerproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerfeedback',
            name='order_item',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_feedback', to='store.foodorderitem'),
        ),
    ]
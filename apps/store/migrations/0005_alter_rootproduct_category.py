# Generated by Django 3.2.6 on 2021-09-23 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210923_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rootproduct',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='root_product', to='store.productcategory', verbose_name='Категория'),
        ),
    ]
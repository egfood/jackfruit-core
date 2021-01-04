# Generated by Django 3.0.7 on 2020-07-06 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200618_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homelocation',
            name='city_type',
            field=models.CharField(choices=[('city', 'город'), ('settlement', 'поселок'), ('village', 'деревня')], default='city', max_length=100, verbose_name='Тип населенного пункта'),
        ),
        migrations.AlterField(
            model_name='homelocation',
            name='street_type',
            field=models.CharField(choices=[('street', 'улица'), ('proezd', 'проезд'), ('avenue', 'проспект'), ('square', 'площадь'), ('side_street', 'переулок'), ('other', 'другое')], default='street', max_length=40, verbose_name='Тип участка города'),
        ),
        migrations.AlterField(
            model_name='officelocation',
            name='city_type',
            field=models.CharField(choices=[('city', 'город'), ('settlement', 'поселок'), ('village', 'деревня')], default='city', max_length=100, verbose_name='Тип населенного пункта'),
        ),
        migrations.AlterField(
            model_name='officelocation',
            name='street_type',
            field=models.CharField(choices=[('street', 'улица'), ('proezd', 'проезд'), ('avenue', 'проспект'), ('square', 'площадь'), ('side_street', 'переулок'), ('other', 'другое')], default='street', max_length=40, verbose_name='Тип участка города'),
        ),
    ]

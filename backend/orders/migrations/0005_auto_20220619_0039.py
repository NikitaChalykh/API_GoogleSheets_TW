# Generated by Django 3.1.14 on 2022-06-18 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_goodsorder_is_sending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsorder',
            name='is_sending',
            field=models.BooleanField(default=False, verbose_name='Статус отправки в телеграмм'),
        ),
    ]

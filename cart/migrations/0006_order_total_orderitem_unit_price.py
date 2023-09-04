# Generated by Django 4.2.4 on 2023-08-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='unit_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
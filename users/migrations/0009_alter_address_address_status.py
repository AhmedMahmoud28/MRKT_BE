# Generated by Django 4.2.4 on 2023-08-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_address_address_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_status',
            field=models.BooleanField(default=False),
        ),
    ]
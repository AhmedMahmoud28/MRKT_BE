# Generated by Django 4.2.4 on 2023-08-30 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_address_address_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'address'},
        ),
    ]
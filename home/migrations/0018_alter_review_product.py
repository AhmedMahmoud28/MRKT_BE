# Generated by Django 4.2.7 on 2023-12-06 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0017_alter_wishlist_product_alter_wishlist_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="home.product"
            ),
        ),
    ]

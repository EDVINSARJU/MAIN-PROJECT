# Generated by Django 4.2.7 on 2023-12-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_order_orderitem_shoppingcart_remove_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
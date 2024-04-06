# Generated by Django 4.2.7 on 2024-03-07 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0019_product_estimated_purity'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('volume', models.FloatField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gold_item', to='userapp.product')),
            ],
        ),
    ]

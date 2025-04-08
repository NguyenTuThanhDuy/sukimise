# Generated by Django 5.2 on 2025-04-07 05:59

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_brand_brand_gin_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='brand',
            name='brand_name_desc_idx',
        ),
        migrations.RemoveIndex(
            model_name='collection',
            name='collection_name_desc_idx',
        ),
        migrations.RemoveIndex(
            model_name='product',
            name='product_name_desc_idx',
        ),
        migrations.RemoveIndex(
            model_name='supplier',
            name='supplier_name_desc_idx',
        ),
    ]

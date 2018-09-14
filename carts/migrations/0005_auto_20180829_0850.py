# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cartitem_line_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='sub_total',
            field=models.DecimalField(default=0.0, max_digits=50, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='line_total_price',
            field=models.DecimalField(max_digits=15, decimal_places=2),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20180819_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='line_total_price',
            field=models.DecimalField(default=19.99, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]

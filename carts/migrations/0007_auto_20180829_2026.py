# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20180829_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_persent',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(default=0.0, max_digits=50, decimal_places=2),
        ),
    ]

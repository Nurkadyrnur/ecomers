# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_auto_20180829_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='tax_persent',
            field=models.DecimalField(default=0.08, max_digits=10, decimal_places=2),
        ),
    ]

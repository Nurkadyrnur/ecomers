# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20180829_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='sub_total',
            field=models.DecimalField(default=0.0, max_digits=50, decimal_places=2),
        ),
    ]

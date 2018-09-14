# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercheckout',
            name='braintree_id',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]

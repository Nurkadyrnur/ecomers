# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20180809_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeatured',
            name='text_css_color',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
    ]

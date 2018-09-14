# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import products.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20180808_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 8, 8, 3, 34, 557615, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_products),
        ),
    ]

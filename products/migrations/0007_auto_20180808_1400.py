# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20180806_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 8, 8, 0, 48, 242679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_products, width_field=500, height_field=500),
        ),
    ]

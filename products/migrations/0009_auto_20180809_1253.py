# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import products.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20180808_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeatured',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(upload_to=products.models.image_upload_products_featured)),
                ('title', models.CharField(max_length=100, blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('text_right', models.BooleanField(default=True)),
                ('text_css_color', models.CharField(max_length=6, blank=True, null=True)),
                ('show_price', models.BooleanField(default=False)),
                ('make_image_background', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
                'verbose_name': 'ProductFeatured',
                'verbose_name_plural': 'ProductFeatureds',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 9, 6, 53, 31, 675115, tzinfo=utc)),
        ),
    ]

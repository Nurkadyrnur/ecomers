# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20180805_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2018, 8, 6, 6, 48, 16, 260328, tzinfo=utc))),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_products),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='products.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='default',
            field=models.ForeignKey(blank=True, null=True, related_name='default_category', to='products.Category'),
        ),
    ]

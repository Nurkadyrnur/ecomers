# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('sale_price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': 'Variations',
            },
        ),
    ]

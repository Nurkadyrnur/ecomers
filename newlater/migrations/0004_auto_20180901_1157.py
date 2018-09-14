# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newlater', '0003_auto_20180729_1342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signup',
            options={},
        ),
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='signup',
            name='full_name',
            field=models.CharField(max_length=120, blank=True, null=True),
        ),
    ]

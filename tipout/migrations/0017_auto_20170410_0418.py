# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-10 04:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipout', '0016_auto_20170410_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='plan',
            field=models.CharField(default='', max_length=16),
        ),
    ]

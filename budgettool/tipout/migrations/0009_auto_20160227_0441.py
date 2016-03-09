# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipout', '0008_auto_20160222_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='note',
            field=models.CharField(default='Expenditure', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='new_user',
            field=models.BooleanField(),
        ),
    ]

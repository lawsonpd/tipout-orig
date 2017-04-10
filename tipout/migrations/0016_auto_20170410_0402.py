# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-10 04:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipout', '0015_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='TipoutUser',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-27 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oral_history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='summary',
            field=models.TextField(blank=True, max_length=15000, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-02 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0030_auto_20180425_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_type',
            field=models.CharField(choices=[(b'CSNAP', b'CSnap'), (b'BLOCK', b'C-Scratch'), (b'SPA', b'SinglePageApplication'), (b'OHP', b'Oral History Project')], max_length=5),
        ),
    ]
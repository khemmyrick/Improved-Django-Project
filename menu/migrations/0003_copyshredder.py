# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-11-08 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='CopyShredder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-06-01 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ('-expiration_date',)},
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
    ]

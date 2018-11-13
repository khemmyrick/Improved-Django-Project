# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-11-13 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_copyshredder'),
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
            options={'ordering': ('-expiration_date', 'season')},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='season',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

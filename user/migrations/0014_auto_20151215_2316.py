# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_profile_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Rank'),
        ),
    ]

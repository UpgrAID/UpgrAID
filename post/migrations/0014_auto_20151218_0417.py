# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_groupmessage_usermessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Group'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20151214_2038'),
        ('post', '0006_post_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='group',
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ManyToManyField(to='user.Group'),
        ),
    ]
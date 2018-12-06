# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-06 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0002_group_show_for_memberships'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='show_for_events',
            field=models.BooleanField(default=True, help_text='If checked, this group will show as an option for the group field on events'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 09:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gptest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menumodel',
            old_name='has_childred',
            new_name='has_children',
        ),
    ]

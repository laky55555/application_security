# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 12:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hw9', '0002_blogcolumnencrypthw9'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcolumnencrypthw9',
            options={'permissions': (('see_post_encrypted', 'Can see post encrypted'), ('create_post_encrypted', 'Can create post encrypted'), ('modifiy_post_encrypted', 'Can change post encrypted'), ('delete_post_encrypted', 'Can remove a post encrypted'))},
        ),
    ]

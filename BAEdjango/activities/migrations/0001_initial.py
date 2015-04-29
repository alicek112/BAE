# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catlist',
            fields=[
                ('category', models.CharField(max_length=100, serialize=False, primary_key=True, db_column='CATEGORY', blank=True)),
                ('description', models.CharField(max_length=1000, null=True, db_column='DESCRIPTION', blank=True)),
                ('resources', models.CharField(max_length=1000, null=True, db_column='RESOURCES', blank=True)),
                ('name', models.CharField(max_length=100, null=True, db_column='NAME', blank=True)),
                ('calendar', models.CharField(max_length=1000, null=True, db_column='CALENDAR', blank=True)),
            ],
            options={
                'db_table': 'catList',
            },
        ),
        migrations.CreateModel(
            name='Mainbae',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True, db_column='NAME', blank=True)),
                ('category', models.CharField(max_length=100, null=True, db_column='CATEGORY', blank=True)),
                ('start', models.DateTimeField(null=True, db_column='START', blank=True)),
                ('end', models.DateTimeField(null=True, db_column='END', blank=True)),
                ('info', models.CharField(max_length=1000, null=True, db_column='INFO', blank=True)),
                ('cancelled', models.IntegerField(null=True, db_column='CANCELLED', blank=True)),
                ('updated', models.IntegerField(null=True, db_column='UPDATED', blank=True)),
            ],
            options={
                'db_table': 'mainBae',
            },
        ),
    ]

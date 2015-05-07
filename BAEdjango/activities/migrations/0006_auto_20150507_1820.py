# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20150507_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Baeuserlist',
            fields=[
                ('netid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('skating', models.BooleanField(default=True)),
                ('watching', models.BooleanField(default=True)),
                ('basketball', models.BooleanField(default=True)),
                ('martial', models.BooleanField(default=True)),
                ('stephens', models.BooleanField(default=True)),
                ('dillon', models.BooleanField(default=True)),
                ('swimming', models.BooleanField(default=True)),
                ('squash', models.BooleanField(default=True)),
                ('tennis', models.BooleanField(default=True)),
                ('running', models.BooleanField(default=True)),
                ('fitness', models.BooleanField(default=True)),
                ('oa', models.BooleanField(default=True)),
                ('dancing', models.BooleanField(default=True)),
                ('biking', models.BooleanField(default=True)),
                ('yoga', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='baeuser',
            name='cats',
        ),
        migrations.RemoveField(
            model_name='baeuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='BaeUser',
        ),
    ]

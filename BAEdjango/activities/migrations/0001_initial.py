# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254, null=True, blank=True)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Catlist',
            fields=[
                ('category', models.CharField(max_length=100, serialize=False, primary_key=True, db_column='CATEGORY', blank=True)),
                ('description', models.CharField(max_length=1000, null=True, db_column='DESCRIPTION', blank=True)),
                ('resources', models.CharField(max_length=1000, null=True, db_column='RESOURCES', blank=True)),
                ('name', models.CharField(max_length=100, null=True, db_column='NAME', blank=True)),
                ('calendar', models.CharField(max_length=1000, null=True, db_column='CALENDAR', blank=True)),
                ('short', models.CharField(max_length=100, null=True, db_column='SHORT', blank=True)),
                ('map', models.CharField(max_length=1000, null=True, db_column='MAP', blank=True)),
            ],
            options={
                'db_table': 'catList',
                'managed': False,
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
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BaeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cats', models.ManyToManyField(to='activities.Catlist')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

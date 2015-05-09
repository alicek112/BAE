# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0002_auto_20150507_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cats', models.ManyToManyField(to='activities.Catlist')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userfavorites',
            name='cats',
        ),
        migrations.RemoveField(
            model_name='userfavorites',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserFavorites',
        ),
    ]

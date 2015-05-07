# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20150507_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baeuser',
            name='user',
            field=models.OneToOneField(to='activities.AuthUser'),
        ),
    ]

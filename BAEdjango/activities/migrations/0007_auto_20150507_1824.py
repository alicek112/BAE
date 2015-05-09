# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20150507_1820'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Baeuserlist',
            new_name='Favorites',
        ),
    ]
